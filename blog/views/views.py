from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, CreateView

from blog.models import Blog


# Create your views here.
class BlogListView(ListView):
    model = Blog
    queryset = Blog.objects.all()
    template_name = 'list.html' # 앱 지정하기 싫으면 그냥 blog 폴더 안에 templates/list.html 하면 된다.

class BlogCreateView(LoginRequiredMixin, CreateView): # 처음에 로그인 기능을 안넣어줘서 테스트에 오류가 발생할것임
    model = Blog
    fields = ('title', 'content', 'published_at')
    template_name = 'form.html'

    # 폼이 valid 할때 어디로 가야할지 지정해주지 않아 status code 에서 오류 발생
    # form_valid 할떄 author 도 넣어줘야함
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        return HttpResponseRedirect(reverse('blog_list'))

    # 이렇게 했는데 에러가 발생하는것은 form에서 에러가나서 그런것일 거임 => null=True, blank= True 를 해주지 않아서 그럼