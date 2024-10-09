from django.urls import path
from . import views


app_name= 'blog'


urlpatterns = [
    path('', views.post_list, name='list'),
    path('detail/<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='detail'),
]