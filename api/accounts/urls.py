from .views import LoginView, UserCreate
from django.urls import path, include

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", UserCreate.as_view(),name="signup")
]
