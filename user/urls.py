from django.urls import path

from .views import (
    Custom_user_register,
    LoginAPIView
)


urlpatterns = [
    path('register',Custom_user_register.as_view(),name="register"),
    path('login',LoginAPIView.as_view(),name="login"),

]

