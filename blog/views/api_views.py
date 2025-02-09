from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Blog
from blog.serializers import BlogSerializer
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from utils.permissions import IsAuthorOrReadOnly


class BlogListCreateAPIView(APIView):
    # permission_classes = [IsAuthenticated] # 이렇게 하면 Get 요청시에도 로그인이 안되어있으면 막힘
    permission_classes = [IsAuthenticatedOrReadOnly] # 읽기만 가능

    def get(self, request, format=None):
        blog_list = Blog.objects.all().order_by('created_at').select_related('author')

        paginator = PageNumberPagination()
        queryset = paginator.paginate_queryset(blog_list, request)

        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data) # serializer 를 장고 form 과 유사하게 사용
        if serializer.is_valid():
            blog = serializer.save(author=request.user)

            # Response : JSON 데이터를 자동으로 직렬화, 클라이언트에게 응답을 반환할 때 사용
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class BlogDetailAPIView(APIView):
    object = None
    permission_classes = [IsAuthorOrReadOnly]
    def get(self, request, format=None, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        serializer = BlogSerializer(blog, many=False)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        serializer = BlogSerializer(blog, data=request.data, partial=True) # 일부만 하는 patch 기에
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        blog.delete()
        return Response({
            'deleted': True,
        }, status.HTTP_200_OK)

    # 자주쓰이니 함수 제작
    def get_object(self, request, *args, **kwargs):
        # PATCH, PUT, DELETE 요청을 여러 번 보낼 때, 같은 데이터를 여러 번 불러오지 않기 위해 self.object를 사용
        if self.object: # permisi
            return self.object
        blog_list  = Blog.objects.all().select_related('author')
        pk = kwargs.get('pk', 0)

        # blog = blog_list.filter(pk=pk).first()
        # if not blog:
        #     raise Http404
        blog = get_object_or_404(blog_list, pk=pk)
        self.object = blog
        return blog




# FBV 로도 만들 수 있음
from rest_framework.decorators import api_view, schema
from rest_framework.schemas import AutoSchema

@api_view(['GET']) # 어떤 요청을 받을건지 작성
@schema(AutoSchema())
def detail_view(request, pk):
    blog_list = Blog.objects.all().select_related('author')

    blog = get_object_or_404(blog_list, pk=pk)

    serializer = BlogSerializer(blog, many=False)
    return Response(serializer.data)


