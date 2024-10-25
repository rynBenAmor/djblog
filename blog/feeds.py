import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post
from django.utils.safestring import mark_safe

class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:list')#use reverse_lazy() because feed definitions are evaluated before URLs are fully loaded.
    description = 'New posts of my blog.'

    def items(self):
        return Post.published.all().order_by('-created')[:5]#latest
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return mark_safe(truncatewords_html(markdown.markdown(item.body), 30))
    def item_pubdate(self, item):
        return item.publish
    