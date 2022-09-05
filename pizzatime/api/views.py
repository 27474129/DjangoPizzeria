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


# базовый класс для обработки и логирования ошибок
class BaseApiView(APIView):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as exception:
            logger.error(exception)
            return Response({"error" : exception})


# к данному классу приложение на телефон должен подвязаться вебхуком в ожидании нового заказа
class GetOrder(BaseApiView):
    # данный класс ожидает на вход pk точки из которой поступает запрос чтобы смотреть новые заказы именно для этой точки
    def get(self, request):
        point_pk = request.GET.get("point_pk")
        # если pk точки не был получен
        if (point_pk is None):
            return Response({
                "success" : "false",
                "error" : "didnt sent point_pk",
            })
        # попытка получения нового заказа для данной точки
        order = Orders.objects.filter(point_pk=point_pk)


        logger.debug(order)
        logger.debug(f"Point primary key: {point_pk}")
        # если новый заказ найден
        return Response({
            "success" : "true",
            "order" : OrdersSerialiser(order[0]).data,
        # если новый заказ не найден
        }) if len(order) != 0 else Response({"order" : "no new orders"})


# класс для изменения статуса заказа
# запросы к url который обрабатывает данный класс будут происходить при:
# 1. получении точкой заказа
# 2. окончании приготовления
# 3. получении заказа доставщиком
# 4. получении заказа заказчиком
class OrderStatusChanging(BaseApiView):
    def get(self, request):
        # ниже идет получение 3х полей из параметров get запроса, все они обязательны
        point_pk = request.GET.get("point_pk")
        order_pk = request.GET.get("order_pk")
        new_status = request.GET.get("new_status")

        # если какое-либо поле не было введено
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
            # попытка найти заказ с pk точки и pk заказа
            order = Orders.objects.filter(point_pk=point_pk, pk=order_pk)
        except Exception as exception:
            logger.debug(exception)
            return Response({
                "success" : "false",
                "error" : str(exception),
            })
        # если не нашлось такого заказа
        if (len(order) == 0):
            return Response({
                "success" : "false",
                "error" : "order is not found",
            })

        # обновление статуса
        order.update(status=new_status)
        if (new_status == "cooking_end"):
            point_object_for_update = Points.objects.filter(pk=point_pk)
            point = Points.objects.filter(pk=point_pk)[ 0 ]
            # удаление одного тукущего заказа из точки
            point_object_for_update.update(current_orders_count=point.current_orders_count - 1)

        return Response({
            "success" : "true",
        })
