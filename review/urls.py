from django.urls import path
from .views      import ReviewView, ReviewDetailView

urlpatterns = [
    path('/<str:product_name>', ReviewView.as_view()),
    path('/<str:product_name>/<int:review_id>/update', ReviewDetailView.as_view()),
]
