from django.urls import path, include
from . import views #   현재 위치에 있는 views

urlpatterns = [
    path('', views.landing),
    path('about_me/', views.about_me),
]