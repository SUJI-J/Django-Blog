from django.urls import path, include
from . import views

urlpatterns = [
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('', views.PostList.as_view()), # server/blog => 모든 걸 검색
    path('<int:pk>/new_comment/', views.new_comment),# /blog/1/new_comment/
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()), # blog/update_comment/1
    path('delete_comment/<int:pk>/', views.delete_comment), # blog/delete_comment/1

    path('<int:pk>/', views.PostDetail.as_view()), # server/blog/1 => 키로 하나만 검 => 지정 안하면 자동으로 Post_detail파일을 찾게됨
    path('category/<str:slug>/', views.category_page), # function 형태로 가장 , slug가 따라옴 -> views 함수에 slug 매개변수 추가
    path('create_post/', views.PostCreate.as_view()), # /blog/create_post/
    path('update_post/<int:pk>/', views.PostUpdate.as_view()) # /blog/update_post/1

    #   path('<int:pk>/', views.single_post_page), #server/blog/1
    #   path('update_post/<int:pk>/', views.PostUpdate.as_view()),

]