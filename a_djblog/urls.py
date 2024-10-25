from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.views.decorators.cache import cache_page #optional

mysitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('sitemap.xml', cache_page(60 * 60)(sitemap), {'sitemaps': mysitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('', RedirectView.as_view(url='/blog/', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)