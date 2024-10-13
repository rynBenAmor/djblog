from django.urls import path
from . import views


app_name= 'blog'


urlpatterns = [
    path('', views.post_list, name='list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='list_by_tag'),
    path('detail/<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='detail'),
    path('<int:id>/share/', views.post_share, name='share'),
    path('<int:post_id>/comment', views.post_comment, name='comment'),
]