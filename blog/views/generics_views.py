
from django.db.models import Q
from django.utils import timezone
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, \
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import Blog, Comment
from blog.serializers import BlogSerializer, CommentSerializer, CommentBlogSerializer


class BlogQuerySetMixin:
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        # 함수를 이렇게 선언해서 넣어야 datetime.now가 그 발생시간에 선언된다. 클래스내에서 만들면 그클래스가 처음에 선언 됬을때 의시간으로 생성됨
        return self.queryset.filter(
            Q(published_at__isnull=True) |
            Q(published_at__gte=timezone.now())
        ).order_by('-created_at').select_related('author')
class BlogListAPIView(BlogQuerySetMixin, ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

from utils.permissions import IsAuthorOrReadOnly
class BlogRetrieveAPIView(BlogQuerySetMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]

class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        blog=self.get_blog_object()
        serializer.save(author=self.request.user, blog = blog)

    def get_queryset(self):
        queryset = super().get_queryset()
        blog = self.get_blog_object()
        return queryset.filter(blog=blog)

    def get_blog_object(self):
        return get_object_or_404(Blog, pk=self.kwargs.get('blog_pk'))

# 상세페이지가 없기에 이렇게 상속받는게 적절함
class CommentUpdateDestroyAPIView(UpdateAPIView,  DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentBlogSerializer
    permission_classes = [IsAuthorOrReadOnly]