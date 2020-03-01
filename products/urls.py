from django.urls import path

from .views import ProductView, ProductDetailView, ProductCategoryView, RecipeView, RecipeDetailView

urlpatterns = [
        path('/collections/', ProductView.as_view()),
        path('/collections/<slug:slug>/', ProductCategoryView.as_view()),
        path('/recipes', RecipeView.as_view()),
        path('/<slug:slug>', ProductDetailView.as_view()),
        path('/recipes/<int:int>', RecipeDetailView.as_view()),
        ]
