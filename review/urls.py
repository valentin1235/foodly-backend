from django.urls import path
from .views import ReviewCreateView, ReviewUpdateView

urlpatterns = [
    path('/<int:product_id>', ReviewCreateView.as_view()),
    path('/<int:product_id>/<int:review_id>/update', ReviewUpdateView.as_view()),
]
