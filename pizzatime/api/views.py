from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from core.models import Orders
from .serializers import OrdersSerialiser
from .models import *
import logging
import io


logger = logging.getLogger("debug")


class BaseApiView(APIView):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as exception:
            logger.error(exception)
            return Response({"error" : exception})


class GetOrder(BaseApiView):
    def get(self, request):
        point_pk = request.GET.get("point_pk")
        if (point_pk is None):
            return Response({
                "success" : "false",
                "error" : "didnt sent point_pk",
            })

        order = Orders.objects.filter(point_pk=point_pk)


        logger.debug(order)
        logger.debug(f"Point primary key: {point_pk}")
        return Response({
            "success" : "true",
            "order" : OrdersSerialiser(order[0]).data,

        }) if len(order) != 0 else Response({"order" : "no new orders"})


class OrderStatusChanging(BaseApiView):
    def get(self, request):
        point_pk = request.GET.get("point_pk")
        order_pk = request.GET.get("order_pk")
        new_status = request.GET.get("new_status")

        if (point_pk is None or order_pk is None or new_status is None):
            errors = []
            if (point_pk is None): errors.append("didnt sent point_pk")
            if (order_pk is None): errors.append("didnt sent order_pk")
            if (new_status is None): errors.append("didnt sent new_status")

            return Response({
                "success" : "false",
                "error" : errors,
            })

        try:
            order = Orders.objects.filter(point_pk=point_pk, pk=order_pk)
        except Exception as exception:
            logger.debug(exception)
            return Response({
                "success" : "false",
                "error" : str(exception),
            })

        if (len(order) == 0):
            return Response({
                "success" : "false",
                "error" : "order is not found",
            })

        order.update(status="cookingg")

        return Response({
            "success" : "true",
        })

