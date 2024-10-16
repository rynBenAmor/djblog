from django import template

from ..models import Post
from django.db.models import Count



register = template.Library()

@register.simple_tag(name="total_posts")
def total_posts():

    return Post.published.count()



@register.inclusion_tag('blog/includes/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}



@register.simple_tag()
def get_most_commented_posts(count=3):
    # Fetch the posts with the most comments, limited to the specified count
    

    return Post.published.annotate(
        total_comments=Count('comments')  # Count the number of comments related to each post
    ).order_by('-total_comments')[:count]  # Order by total_comments in descending order and limit results


import markdown
from django.utils.safestring import mark_safe

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

"""
@register.simple_tag()
def id_is_pair(count=5):
    posts_id_pair = Post.published.annotate(
        is_pair=Case(
            When(id__mod=2, then=Value('Even')),
            default=Value('Odd'),
            output_field=CharField(),
        )
    )[:count]  # Limits to 'count' number of posts
    return posts_id_pair
"""