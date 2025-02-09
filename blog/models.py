# blog/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Manager
from django.utils import timezone

from utils.models import TimestampModel

User = get_user_model()

class PublishedManager(Manager): # objects 에 적용시키기 위한 것
    def get_queryset(self):
        now = timezone.now()

        from django.db.models import Q
        return super().get_queryset().filter(
            Q(published_at__isnull=True) | # 즉시활성화된글 publihsed_at = None
            Q(published_at__lte=now), # 현재시간보다 이전에 배포된 글
        )

class Blog (TimestampModel) :
    title = models. CharField('제목', max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_at = models.DateTimeField('배포일시', null=True, blank=True)

    objects = PublishedManager() # ✅ 기본 objects를 PublishedManager로 설정
    all_objects = Manager() # ✅ 모든 Blog 데이터를 가져오는 매니저 (기본 Manager)

    @property
    def is_active(self) : # 배포가 된지 안된지 판단하는 부분
        now = timezone.now()

        if not self.published_at :
            return True

        return self.published_at <= now

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'
        ordering = ('-created_at', '-id')


class Comment(TimestampModel) :
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField('본문')

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural ='댓글 목록'
        ordering = ('-created_at', '-id')