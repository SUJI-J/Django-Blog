"""Django_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

#    아무것도 안쓰고 서버 페이지 접속하면 admin로 접속
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('single_pages.urls')),
    path('blog/', include('blog.urls')), #blog  라고 쓰면 어디로 접속되게 할 건지
]
