from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.PostList.as_view()), #server/blog => 모든 걸 검색
    path('<int:pk>/', views.PostDetail.as_view()), #server/blog/1 => 키로 하나만 검 => 지정 안하면 자동으로 Post_detail파일을 찾게됨
    #path('<int:pk>/', views.single_post_page), #server/blog/1
]