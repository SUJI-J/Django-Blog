from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.CartList.as_view()), # 장바구니 페이지
    path('product/<int:pk>/buy_product/', views.buyProduct), # 구매가 이루어지는 페이지
    path('product/<int:pk>/', views.ProductDetail.as_view()), # 구매 수량 입력 페이지
    path('product/', views.ProductList.as_view()), # 상품보기 페이지
    path('', views.index), # 첫 페이지
]