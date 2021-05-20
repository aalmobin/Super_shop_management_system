from django.urls import path
from .views import Home, About, Contact, AddToCart, MyCart, ManageCart, EmptyCart, CheckOut, ShowOrder
from .import views

app_name = 'core'

urlpatterns = [
    path('', Home.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),
    path('contact/', Contact.as_view(), name='contact'),
    path('add-to-cart/<int:pk>/', AddToCart.as_view(), name='add-to-cart'),
    path('my-cart/', MyCart.as_view(), name='my-cart'),
    path('manage-cart/<int:pk>/', ManageCart.as_view(), name='manage-cart'),
    path('empty-cart', EmptyCart.as_view(), name='empty-cart'),
    path('check-out/', CheckOut.as_view(), name='check-out'),
    path('orders/', ShowOrder.as_view(), name='orders'),
    path('invoice/<int:pk>/', views.downpdf, name='invoice'),
]
