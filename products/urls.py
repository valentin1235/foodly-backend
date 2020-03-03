from django.urls import path

from .views import ProductView , SearchView

urlpatterns = [
    path('/all-products', ProductView.as_view()),
    path('/search' , SearchView.as_view())
]
