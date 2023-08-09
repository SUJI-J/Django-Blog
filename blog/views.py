from django.shortcuts import render, redirect
from .models import Post, Category, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q


# models.py안에 Post 만들어 놓음
# Create your views here

# def : FBV (return render) / class : CBV - as_viewn (model = Post)

# templates : user
# 함수 : request.user
# 클래스 : self.request.user

def csrf_failure(request, reason=""):
    return redirect('/blog/')
    # 토큰 오류 방지 / 404 forbidden


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    # template_name = "blog/post_update_form.html"
    # default templated_name => post_form.html
    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class PostCreate(LoginRequiredMixin, UserPassesTestMixin,
                 CreateView):  # Form 지원 / Form Class / form이긴 하지만 view를 상속 받아서 만든거임
    model = Post
    # post model에 있는 변수명이랑 똑같이 해주면 댐
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    # blog/create_post 들어가면 post_form.html찾음
    # template_name = 'blog/post_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user  # 로그인 되어잇는 사용자
            # not tag
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')


class PostList(ListView):
    # post_list 가 변수가 됨 여기에 리스트를 전부 가져오겠다는 거임 / pk 역순으로 / postlist형태로 자동으로 넘어감
    # CBV 방식
    model = Post  # post_list 변수
    ordering = '-pk'
    paginate_by = 2  # 알아서 한 페이지 당 두개씩 보이게 해줌

    # 추가 context-Category 해서 넘겨줌 => detail도 마찬가지
    # template_name = 'blog/old_post_list.html' =>    대신 index.html를 post_list.html로 바꿔주면 됨
    # urls.py에서 views.py 호출 해줌
    # 자동으로 모델명_list.html를 찾도록 강제적으로 명령되어있음
    # 수동으로 조정해줄 수 있음

    def get_context_data(self, **kwargs):
        # listview에서 자동으로 부름 -> post_list가 자동으로 넘어감
        context = super(PostList, self).get_context_data()

        # 카테고리 테이블에 들어있는 데이터를 카테고리즈 라는 변수에 넣어서 넘겨라
        context['categories'] = Category.objects.all()

        # post에서 카테고리가 없는 것의 개수를 가져오자 -> 1개면 1이라는 숫자를 노카테고리 포스트 카운트에 저장
        context['no_category_post_count'] = Post.objects.filter(category=None).count()

        # 이게자동으로 post_list.html에 넘어감 , { post_list, categories, no_category_post_count }  = { 7, 4, 1 } / 포스트개수 , 카테고리 분류, 미분류개수
        return context


class PostDetail(DetailView):  # post_detail.html을 자동적으로 찾게 됨
    model = Post

    #   template_name = 'blog/single_post_page.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()  # post 라는 하나의 값만 넘어감 , post
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context


def category_page(request, slug):
    if slug == 'no_category':  # /blog/category/no_category/
        category = "No Category"
        post_list = Post.objects.filter(category=None)
    else:  # /blog/category/slug(프로그래밍, 문화-예술, 라이프스타일)
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,  # 현재 분류 카테고리를 카테고리에 넣어서 보내
        }
    )


# comment
def new_comment(request, pk):
    if request.user.is_authenticated:
        # 하나의 객체만 가져오는 함수가 작성되어 있으니까 그걸 이용하자, Post모델에서 번호에 해당되는 한개만 가져오자
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)  # 임시저장
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    # 로그인 + 댓글 삭제 요청한 사람 == 댓글 작성자 본인이면 댓글 삭제 가능
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment  # 다섯개나 갖고 있음 -> CommentForm을 만들어놨으니 그걸 가져다 쓰자, Cotent하나 있음
    form_class = CommentForm

    # templates => comment_form.html

    # POST 방식인지 GET 방식인지 확인하는 함수
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:  # get_object : Comment
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class PostSearch(PostList):
    paginate_by = None  # PostList에서 지정했던 페이지네이션은 필요없으므로 None으로 지정

    def get_queryset(self):
        q = self.kwargs['q'] # urls.py에서 인자로 받아온 값을 가져올 때 사용
        post_list = Post.objects.filter(
            Q(title__contains=1) | Q(tags__name__contains=q) # 여러 조건을 사용하고 싶을 때 Q 사용 / tag__name__contains == tag.name.contains
        ).distinct() # 중복 제거
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context

# 얘 대신 위에 클래스로 이용해바 ~
# FBV 방식
# def index(request):
#     #   포스팅 되어있는 하나하나가 object임 / DB에 있는 거 가져옴 / pk의 역순으로 가져와라
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'blog/old_post_list.html',
#         #   데이터 넘길 땐 {} 중괄호로 / 앞: (index.html로 넘기는)변수명 지정 / 뒤: 위에서 오브젝트 받았던 리스트
#         {
#             'posts': posts,
#         }
#     )
#
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk) #데이터 베이스 가서 하나만 가져와
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post': post,
#         }
#     )
