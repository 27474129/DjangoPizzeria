from django.urls import path
from .views import *

urlpatterns = [
    path("", IndexPage.as_view(), name="index"),
    path("order/", Order.as_view(), name="order"),
]
