from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, ListView, TemplateView, CreateView
from django.contrib import messages
from .models import *
from .forms import CheckOutForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from num2words import num2words


class Home(ListView):
    """The index page View"""

    model = Product
    template_name = 'core/index.html'
    context_object_name = 'products'


class AddToCart(TemplateView):
    """The Add to cart View"""

    template_name = 'core/addtocart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from the requested url
        product_id = self.kwargs['pk']
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj
            )
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                product_obj.in_stock -= 1
                product_obj.save()
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
            else:
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.price,
                                                         quantity=1, subtotal=product_obj.price)
                cart_obj.total += product_obj.price
                cart_obj.save()
                product_obj.in_stock -= 1
                product_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(cart=cart_obj, product=product_obj, rate=product_obj.price,
                                                     quantity=1, subtotal=product_obj.price)
            cart_obj.total += product_obj.price
            product_obj.in_stock -= 1
            product_obj.save()
            cart_obj.save()

        return context


class MyCart(TemplateView):
    """The Cart page View"""

    template_name = 'core/mycart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


class ManageCart(View):
    """The manage cart view"""

    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['pk']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == 'inc':
            if cp_obj.product.in_stock != 0:
                cp_obj.quantity += 1
                cp_obj.subtotal += cp_obj.rate
                cp_obj.save()
                cp_obj.product.in_stock -= 1
                cp_obj.product.save()
                cart_obj.total += cp_obj.rate
                cart_obj.save()
                messages.success(request, f'Another {cp_obj.product.title} added')
            else:
                messages.success(request,f'The Product {cp_obj.product.title} is out of stock now')

        elif action == 'dec':
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cp_obj.product.in_stock += 1
            cp_obj.product.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == 'rmv':
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.product.in_stock += cp_obj.quantity
            cp_obj.product.save()
            cp_obj.delete()
        else:
            pass
        return redirect('core:my-cart')


class EmptyCart(View):
    """The Empty cart View"""

    def get(self, request, *args, **kwargs):
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            for cp in cart.cartproduct_set.all():
                cp.product.in_stock += cp.quantity
                cp.product.save()
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect('core:my-cart')


class CheckOut(CreateView):
    """The Checkout page View"""

    template_name = 'core/checkout.html'
    form_class = CheckOutForm
    success_url = reverse_lazy('core:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.total = cart_obj.total
            del self.request.session['cart_id']
            messages.success(self.request, f'Your Order is submitted You can see the invoice from orders')
        else:
            return redirect('core:index')
        return super().form_valid(form)


class ShowOrder(ListView):
    """The order list page View"""

    model = Order
    template_name = 'core/orders.html'
    context_object_name = 'orders'
    ordering = ['-created_at']


def downpdf(request, *args, **kwargs):
    pk = kwargs.get('pk')
    order_obj = get_object_or_404(Order, pk=pk)
    total_in_words = (num2words(order_obj.total))
    template_path = 'core/invoice.html'
    context = {'order_obj': order_obj, 'total_in_words': total_in_words}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


class Contact(View):
    """The Contact page View"""

    def get(self, request, *args, **kwargs):
        return render(request, 'core/contact.html')


class About(View):
    """The About page View"""

    def get(self,  request, *args, **kwargs):
        return render(request, 'core/about.html')
