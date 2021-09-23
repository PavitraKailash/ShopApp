from django.urls import path, include
from .views import *
from django.conf.urls import url

createCart = AddToCartView.as_view({'post': "create_cart"})
decrementCart = AddToCartView.as_view({'post': 'decrement_cart'})
emptyCart = AddToCartView.as_view({'post': 'empty_cart'})
checkout = CheckoutOrderView.as_view({'get': 'getOrderDetails'})
orderFinal = CheckoutOrderView.as_view({'post': 'confirmOrderDetails'})

urlpatterns = [
    path('createuser/', UserViewSet.as_view(), name="User Creation"),
    path('product/', ProductViewset.as_view(), name="Product details"),
    path('product/<int:pdt_id>', ProductViewset.as_view(), name="Product details"),
    path('product-list/', ProductListView.as_view(), name="product list view"),
    path('add-cart/', createCart),
    path('decrement-cart/<int:pdt_id>/', decrementCart),
    path('empty-cart/<int:pdt_id>/', emptyCart),
    path('order-item/', checkout),
    path('order-final/', orderFinal)
]
