from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Blog, Comment

User = get_user_model()

# Form과 비슷한 역할
# 리턴하는 항목들도 필드에 적은 항목들만 리턴하도록 설계되어 있음, 스키마의 역할도 하는것
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)


class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    # read_only => 해당필드를 클라이언트가 수정할 수 없게 해놓는 것
    # foreignkey 연결된것 연결하는것 serialzer 로 해놓은것 이렇게 사용가능
    # 이렇게 쓰면 꼭 까먹지말고 views 에서 select_related 등록하기

    comment_count = serializers.SerializerMethodField()  # 이렇게 쓰면 상페이지에서 댓글 숫자를 확인할수있음
    # SerializerMethodField 메소드는 변수 앞에 get_ 을 붙여 함수로 만들면 변수를 Meta에서 사용하게 해주는 메소드이다
    author_name = serializers.SerializerMethodField()
    def get_comment_count(self, obj):
        return obj.comment_set.count()
    def get_author_name(self, obj):
        return obj.author.username

    # author의 name 만 보면 되어서 이제 author 를 빼도 author를 확인할 수 있다.
    class Meta:
        model = Blog
        fields = ['title', 'content', 'author', 'published_at', 'created_at',
                  'updated_at', 'comment_count','author_name']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', ]

class CommentBlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    blog = BlogSerializer(many=False, read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'author', 'content','blog' ]