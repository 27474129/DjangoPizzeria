from django.urls import path
from .views import *


urlpatterns = [
    path("get_order/", GetOrder.as_view()),
    path("order_status_changing/", OrderStatusChanging.as_view()),
]
