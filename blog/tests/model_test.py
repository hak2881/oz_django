from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from blog.models import Blog

# blog/test.py

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

    def test_blog_is_published(self): # `test_` 가 없으면 일반 함수인지 알고 안도니까 주의
        published_blog = Blog.objects.get(title='배포')
        # unpublished_blog = Blog.objects.get(title='아직 배포안됨') # 이제 objects에서는 가져올 수 없음
        unpublished_blog = Blog.all_objects.get(title='아직 배포안됨') # all_objects를 사용

        self.assertEqual(published_blog.is_active, True)
        self.assertEqual(unpublished_blog.is_active, False) # True면 오류발생
# 📌 assertEqual(a, b)는 두 값이 같은지 확인하는 테스트 함수
# 	•	unittest.TestCase에서 제공하는 단위 테스트 메서드입니다.
# 	•	a와 b의 값이 동일하면 테스트가 통과 ✅
# 	•	값이 다르면 테스트 실패 ❌
#
# self.assertEqual(a, b, "오류 메시지")
#
# •    a == b → ✅ 테스트
# 성공
# •    a != b → ❌ 테스트
# 실패(오류 발생)
    def test_blog_manager(self):
        object_count = Blog.objects.count()
        all_object_count = Blog.all_objects.count()

        self.assertEqual(object_count, 1)
        self.assertEqual(all_object_count, 2)