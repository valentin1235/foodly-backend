from django.urls import path
from .views import WishListCreateView, CartView

urlpatterns = [
    path('/wishlist', WishListCreateView.as_view()),
    path('/cart', CartView.as_view()),
    ]
