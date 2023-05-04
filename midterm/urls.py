from django.urls import path, include
from . import views
#   http://127.0.0.1:8000/midterm/
urlpatterns = [
    path('', views.index),
    path('list/', views.StaffList.as_view()),
    path('list/<int:pk>/', views.StaffCard.as_view()),
    path('list/<int:pk>/alter/', views.StaffCard2.as_view()),

    #path('<int:pk>/', views.name_card.as_view()),
    #path('<int:pk>/', views.name_card2.as_view()),
]