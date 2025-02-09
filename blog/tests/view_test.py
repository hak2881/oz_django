from datetime import datetime, timedelta
from http.client import responses

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import Blog

# blog/view_test.py

class BlogModelTestCase(TestCase):
    # 모델이 이 잘 만들어진지
    def setUp(self): # 테스트 데이터를 생성하는 곳, 아래보다 먼저
        user = User.objects.create(
            username='test',
            is_active=True
        )
        Blog.objects.create(
            title='배포',
            content='본문',
            author=user,
            # 우리가 만들어놓은 is_active 함수가 없으면 True로 해놨기에 배포 되어있음
        )

        future_published_at = timezone.now() + timedelta(days=30)
        Blog.objects.create(
            title='아직 배포안됨',
            content='본문',
            author = user,
            # 현재시간보다 많은 것을 배포날짜로 넣엇기에 is_active가 false일 것임
            published_at=future_published_at
        )

    def test_blog_list(self):
        response = self.client.get(reverse('blog_list'))

        blog_list = Blog.objects.all()
        # status code
        self.assertEqual(response.status_code, 200)
        # context
        self.assertEqual(response.context.get('blog_list').count(), blog_list.count())

    def test_blog_create_not_login(self):
        response = self.client.post(reverse('blog_create'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], settings.LOGIN_URL + '?next=/create/')

    def test_blog_create(self):
        user=User.objects.first()
        self.client.force_login(user) # 로그인 한것처럼 처리

        blog_count = Blog.objects.count() # 기존의 블로그 개수

        response = self.client.post(
            reverse('blog_create'),
            data={
                'title':'제목',
                'content':'본문',
                'published_at': '' # 배포일시 없음 -> 즉시 게시
            }
        )

        self.assertEqual(response.status_code, 302) # 생성후 리다이렉트가 발생되어야 함
        self.assertEqual(response['location'], reverse('blog_list')) # 정상적으로 리스트 페이지로 이동했는지 확인
        self.assertEqual(blog_count + 1, Blog.objects.all().count()) # 생성되엇으므로 기존보다 + 1

        all_count = Blog.all_objects.count()

        self.client.post(
            reverse('blog_create'),
            data={
                'title': '제목',
                'content': '본문',
                'published_at': timezone.now() + timedelta(days=2) # 아직 게시되지 않은 상태
            }
        )
        # 위에서 확인했으니 카운트가 안늘어나는지만 확인
        self.assertEqual(blog_count + 1, Blog.objects.all().count())  # 여기는 나타나지 않았으니 기존 + 1 이 끝
        self.assertEqual(all_count + 1, Blog.all_objects.all().count())

        self.client.post(
            reverse('blog_create'),
            data={
                'title': '제목',
                'content': '본문',
                'published_at': timezone.now() - timedelta(days=2) # 이전이니 게시
            }
        )

        self.assertEqual(blog_count + 2, Blog.objects.all().count()) # 게시한것 = 기존 + 2
