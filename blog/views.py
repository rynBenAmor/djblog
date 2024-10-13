from .models import Post
from taggit.models import Tag
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


def post_list(request, tag_slug=None):    
    posts = Post.published.all()

    tag = None
    if tag_slug:#if tag_slug is not None
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    # Pagination with 3 posts per page
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    
    try:
        # Get the correct page
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page
        posts = paginator.page(paginator.num_pages)
    
    # Updated context to include paginated posts
    context = {
        'posts': posts,
        'tag': tag,
    }
    
    return render(request, 'blog/post_list.html', context)



def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,  # Filter for only published posts
        slug=post,  # Match the slug from the URL
        publish__year=year,  # Match the year
        publish__month=month,  # Match the month
        publish__day=day  # Match the day
    )

    # List of active comments for this post using related_name=
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    
    context = {
        'post': post,
        'comments': comments,
        'form':form,
        }
    return render(request, 'blog/post_detail.html', context)



def post_share(request, id):
    # Fetch the post by its ID, making sure it has a 'PUBLISHED' status.
    # If the post is not found, a 404 (Not Found) error will be raised.
    post = get_object_or_404(Post, id=id,)

    # 'sent' is used to track if the email has been successfully sent.
    # Initially, it's set to False, and later updated to True upon success.
    sent = False

    # Check if the request method is POST, which means the form has been submitted.
    if request.method == 'POST':
        # Create an instance of the form with the submitted POST data.
        form = EmailPostForm(request.POST)
        
        # Check if the form is valid (i.e., it passes all validation checks).
        if form.is_valid():
            # form.cleaned_data is a dictionary that contains the sanitized and validated form data.
            # We use it to safely extract the data that was submitted.
            cd = form.cleaned_data
            
            # Build the absolute URL for the blog post being shared.
            # 'post.get_absolute_url()' returns the relative URL to the post,
            # and 'request.build_absolute_uri()' constructs the full URL (including domain).
            post_url = request.build_absolute_uri(post.get_absolute_url())

            # Create the email subject. This includes the sender's name and email, as well as the post title.
            # 'cd['name']' and 'cd['from_email']' are taken from the validated form data.
            subject = (
                f"{cd['name']} ({cd['from_email']}) "
                f"recommends you read {post.title}"
            )

            # Create the email message. This contains the post's URL, title, and any comments the sender added.
            # The comments are optional, but if provided, they are included in the message.
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )

            # Send the email using Django's 'send_mail' function.
            # 'subject' is the email subject, 'message' is the email body, and 'recipient_list' is the list of recipients.
            # The 'from_email' is set to None, meaning Django will use the default email address from the settings.
            # The recipient list comes from the form data (cd['to_email']).
            send_mail(
                subject=subject,
                message=message,
                from_email=None,  # Uses the default email from settings
                recipient_list=[cd['to_email']]
            )

            # If the email was sent successfully, update 'sent' to True.
            sent = True
        

    else:
        # If the request method is GET, it means the user is visiting the page to fill out the form.
        # We create an empty form to be displayed in the template.
        form = EmailPostForm()

    # Prepare the context dictionary with the post, the form, and whether the email was sent.
    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }

    # Render the 'post_share.html' template with the given context.
    return render(request, 'blog/post_share.html', context)
    



@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)#not yet, we have the fk field missing
        #always assing the whole object , django will deal with the fk id thing
        comment.post = post
        comment.save()
    else:
        form = CommentForm(instance=request.POST)
    
    context={
        'post':post,
        #'form':form, 
        'comment':comment,
    }

    return render(request, 'blog/comment.html', context)
    
