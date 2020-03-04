from django.urls import path
from .views import AddressCreateView, AddressUpdateView, SignUpView, SignInView , KakaoLoginView

urlpatterns = [
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view()),
    path('/address_create', AddressCreateView.as_view()),
    path('/address_update/<int:address_id>', AddressUpdateView.as_view()),
    path('/kakao_signin',KakaoLoginView.as_view())
]
