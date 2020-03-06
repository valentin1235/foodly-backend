from django.urls import path
from .views      import CartView, OrderView, WishListView, ReceiptView

urlpatterns = [
    path('/wishlist', WishListCreateView.as_view()),
    path('/cart', CartView.as_view()),
    path('/checkout', OrderView.as_view()),
    path('/receipt', ReceiptView.as_view())
]
