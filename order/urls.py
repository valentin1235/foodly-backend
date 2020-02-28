from django.urls import path
from .views import WishListCreateView

urlpatterns = [
    path('/wishlist', WishListCreateView.as_view()),
    ]
