# blog/urls/generics_urls.py
from django.urls import path, include
from blog.views import generics_views

app_name ='generics_api'
# blog/urls/api_urls.py
urlpatterns = [
    path('blog', generics_views.BlogListAPIView.as_view(), name='blog_list'),
    path('blog/<int:pk>', generics_views.BlogRetrieveAPIView.as_view(), name='blog_detail'),
    path('/blog/<int:blog_pk>/comment', generics_views.CommentListCreateAPIView.as_view(), name='comment_list_create'),
    path('comment/<int:pk>',generics_views.CommentUpdateDestroyAPIView.as_view(), name='comment_update_delete'),
]