from django.urls import path

from .views import ProductView, ProductDetailView

urlpatterns = [
        path('/all-products', ProductView.as_view()),
        path('/all-products/<slug:slug>', ProductDetailView.as_view()),
        ]
