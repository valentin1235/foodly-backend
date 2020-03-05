from django.urls import path

from .views import ProductView, ProductDetailView, ProductCategoryView, RecipeView, RecipeDetailView, BundleView

urlpatterns = [
        path('/collections', ProductView.as_view()),
        path('/collections/<slug:category_name>', ProductCategoryView.as_view()),
        path('/<int:product_id>', ProductDetailView.as_view()),
        path('/recipes', RecipeView.as_view()),
        path('/recipes/<int:recipe_id>', RecipeDetailView.as_view()),
        path('/promotion', BundleView.as_view())
        ]
