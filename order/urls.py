from django.urls import path
from .views import WishListCreateView, CartView, OrderView

urlpatterns = [
    path('/wishlist', WishListCreateView.as_view()),
    path('/cart', CartView.as_view()),
    path('/checkout', OrderView.as_view()),
    ]
