from django.urls import path, include
from blog.views.api_views import BlogListCreateAPIView, BlogDetailAPIView

app_name ='api'
# blog/urls/api_urls.py
urlpatterns = [
    path('blog', BlogListCreateAPIView.as_view(), name='blog_list'),
    path('blog/<int:pk>', BlogDetailAPIView.as_view(), name='blog_detail'),
    path('blog/fbv/<int:pk>', BlogDetailAPIView.as_view(), name='blog_detail_fbv'),
]