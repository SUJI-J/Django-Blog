from django.shortcuts import render, redirect
from django.views.generic import ListView,DetailView
from .models import Product, Sale
from .forms import ProductForm
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

# Create your views here.

def index(request):
    return render(
        request,
        'final4/index.html'
    )

class ProductList(ListView):
    model = Product
    ordering = '-pk'
    paginate_by = 3
    template_name = 'final4/product_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data()
        return context

class ProductDetail(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data()  # post 라는 하나의 값만 넘어감 , post
        context['product_form'] = ProductForm
        return context

def buyProduct(request, pk):
    if request.user.is_authenticated:
        # 하나의 객체만 가져오는 함수가 작성되어 있으니까 그걸 이용하자, Post모델에서 번호에 해당되는 한개만 가져오자
        product = get_object_or_404(Product, pk=pk)

        if request.method == 'POST':
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                Sale = product_form.save(commit=False)  # 임시저장
                Sale.product = product
                Sale.user = request.user
                Sale.save()
                return redirect(Product.get_absolute_url())
        else:
            return redirect(Product.get_absolute_url())
    else:
        raise PermissionDenied

class CartList(ListView):
    model = Sale
    template_name = 'final4/sale_list.html'

    def get_context_data(self, **kwargs):
        context = super(CartList, self).get_context_data()  # post 라는 하나의 값만 넘어감 , post
        context['product_name'] = Sale.objects.all()
        context['product_form'] = ProductForm
        context['sale_name'] = Sale.product
        context['sale_count'] = Sale.count
        return context