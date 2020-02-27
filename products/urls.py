from django.urls import path

from .views import ProductView

urlpatterns = [
        path('/all-products', ProductView.as_view()),
        ]
