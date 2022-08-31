from django.urls import path
from .views import *

urlpatterns = [
    path("reg", Reg.as_view(), name="reg"),
    path("auth", Auth.as_view(), name="auth"),
    path("logout/", LogoutPage.as_view(), name="logout"),
]