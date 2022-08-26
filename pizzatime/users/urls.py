from django.urls import path
from .views import *

urlpatterns = [
    path("reg", RegPage.as_view(), name="reg"),
    path("auth/", AuthPage.as_view(), name="auth"),
    path("index/", index, name="index"),
]