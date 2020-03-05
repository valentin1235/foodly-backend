from django.urls import path
from .views import CartView, OrderView

urlpatterns = [
    # path('/wishlist', WishListView.as_view()),
    path('/cart', CartView.as_view()),
    path('/checkout', OrderView.as_view()),
]
