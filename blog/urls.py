from django.urls import path
from . import views


app_name= 'blog'


urlpatterns = [
    # If the slug is present, show a specific post; if not, show all posts
    path('', views.post_list, name='list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='list_by_tag'),

    path('detail/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.post_detail, name='detail'),
    path('<int:id>/share/', views.post_share, name='share'),
    path('<int:post_id>/comment', views.post_comment, name='comment'),
]