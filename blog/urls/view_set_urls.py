from django.urls import path, include
from rest_framework import routers

from blog.views import api_view_set_views

app_name ='view_set_api'

router = routers.DefaultRouter(trailing_slash=False) # trailing_slash = False 슬래쉬가 있는지 없는지

router.register(r'users', api_view_set_views.UserViewSet, basename='user')
# prefix 에서 users 를 붙인것은 include에서 users 로 시작하라는 거와 같음 앞에 무조건 /api/users 라 한것임
# viewset이기에 사실 여러개의 페이지를 연결한 것임, 현재 list, detail 페이지
router.register(r'blogs', api_view_set_views.BlogViewSet, basename='blog')


urlpatterns = [
    # path('', api_views.blog_list, name='blog_list'),
    path('',include(router.urls)),
]