from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.PostList.as_view()), #server/blog
    path('<int:pk>/', views.single_post_page), #server/blog/1
]