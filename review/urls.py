from django.urls import path
from .views import ReviewCreateView, ReviewUpdateView

urlpatterns = [
    path('/<str:product_name>', ReviewCreateView.as_view()),
    # path('/<str:product_name>/<int:review_id>/update', ReviewUpdateView.as_view()),
]
