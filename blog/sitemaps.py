from django.contrib.sitemaps import Sitemap
from .models import Post

#The Post model a get_absolute_url() method, so Django handles URL generation for you.
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):#obj returned by item()
        return obj.updated#obj here is the post and updated is an attribute