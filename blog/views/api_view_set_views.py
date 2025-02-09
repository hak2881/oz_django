import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from blog.models import Blog
from blog.serializers import UserSerializer, BlogSerializer

User = get_user_model()
@csrf_exempt
def blog_list(request):
    if request.method == 'GET':
        blogs = Blog.objects.all()

        data = {
            'blog_list': [{'id': blog.id, 'title': blog.title} for blog in blogs]
        }
        return JsonResponse(data, status=200)
    else:
        body = json.loads(request.body.decode('utf-8'))

        blog = Blog.objects.create(
            **body, # 딕셔너리를 위에 작성해놓으면 맞추숴 넣어짐
            author=User.objects.first()
        )

        data = {
            'id' : blog.id,
            'title' : blog.title,
            'content' : blog.content,
            'author' : blog.author.username
        }
        return JsonResponse(data, status=201) # 생성이기에 201 create

from rest_framework import viewsets
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
# viewsets: REST FRAMEWORK 의 특별한 기능
# ReadOnlyModelViewSet : List와 Detail의 API를 만들어줌
# ModelViewSet: : List, Detail, Put, Create, Delete, Fetch 가능

class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Blog.objects.all().order_by('-created_at').select_related('author')
    serializer_class = BlogSerializer
