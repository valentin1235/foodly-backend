from django.urls import path

from .views import ProductView, ProductDetailView, ProductCategoryView

urlpatterns = [
        path('/collections', ProductView.as_view()),
        path('/<slug:slug>', ProductDetailView.as_view()),
        path('/collections/<slug:slug>', ProductCategoryView.as_view())
        ]
