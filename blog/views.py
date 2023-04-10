from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView

#   models.py안에 Post 만들어 놓음

# Create your views here
class PostList(ListView):
    model = Post    #   post_list 가 변수가 됨 여기에 리스트를 전부 가져오겠다는 거임 / pk 역순으로
    ordering = '-pk'
    #   template_name = 'blog/post_list.html' =>    대신 index.html를 post_list.html로 바꿔주면 됨

    #   urls.py에서 views.py 호출 해줌
    #   자동으로 모델명_list.html를 찾도록 강제적으로 명령되어있음
    #   수동으로 조정해줄 수 있음

'''
얘 대신 위에 클래스로 이용해바 ~ 
def index(request):
    #   포스팅 되어있는 하나하나가 object임 / DB에 있는 거 가져옴 / pk의 역순으로 가져와라
    posts = Post.objects.all().order_by('-pk')

    return render(
        request,
        'blog/post_list.html',
        #   데이터 넘길 땐 {} 중괄호로 / 앞: (index.html로 넘기는)변수명 지정 / 뒤: 위에서 오브젝트 받았던 리스트
        {
            'posts': posts,
        }
    )
'''

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)
    return render(
        request,
        'blog/single_post_page.html',
        {
            'post': post,
        }
    )