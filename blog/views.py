from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .forms import EmailPostForm




def post_list(request):
    # Retrieve all published posts
    posts = Post.published.all()
    
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
        'posts': posts
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
    
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)



def post_share(request, id):
    post = get_object_or_404(Post, id=id, status=Post.status.PUBLISHED)

    if request.method == 'POST':#post request means i filled my form
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            

    else:#get request means gimme a form
        form = EmailPostForm()
    
    context = {
        'post':post,
        'form': form
    }

    return render(request, 'blog/post_share.html', context)
        