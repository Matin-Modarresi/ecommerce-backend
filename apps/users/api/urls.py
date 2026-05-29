from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ChangePasswordView,
    LoginView,
    MeView,
    RegisterView
)

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", MeView.as_view(), name="me"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    # مسیر لاگین (دریافت توکن)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # مسیر رفرش کردن توکن
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]