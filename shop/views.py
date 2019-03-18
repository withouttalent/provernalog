from django.shortcuts import render
from provernalog.forms import OrderForm
from .models import Order, Product
# Create your views here.


def order(request, product_id):
    product = Product.objects.get(pk=product_id)
    cadastral_number = request.GET.get('cadastral_number')
    form = OrderForm({'cadastral_number': cadastral_number})
    context = {'Title': f'Товар №{product.id}',
               'product': product,
               'form': form}
    return render(request, 'shop/order.html', context)


def capture(request):
    pass


def index(request):
    context = {
        'products': Product.objects.all(),
        'Title': 'Товары'
    }
    return render(request, 'shop/index.html', context)
