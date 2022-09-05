from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, FormView
from users.forms import RegForm, AuthForm
from .models import Products, Orders
from .forms import *
from django.http import HttpResponseRedirect
from api.models import Points, Deliveries

import logging


logger = logging.getLogger("debug")


# Базовый класс для обработки ошибок в процессе работы других классов
# Каждый класс предствления должен наследоваться от этого базового класса
class BaseView(View):

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as exception:
            logger.error(exception)
            return HttpResponseRedirect(reverse_lazy("index"))


# Класс который содержит в себе логику выгрузки товаров из бд, формы авторизации и регистрации
class IndexPage(BaseView, CreateView, ListView):
    def __init__(self):
        self.form_class = AuthForm
        self.template_name = "core/index.html"
        self.model = Products
        self.success_url = reverse_lazy("index")
        self.context_object_name = "goods"

        # поле в котором хранится информация о том смог ли пользователь авторизоваться
        # используется на 65 строке при образовании контекса
        self.invalid_auth_data = False
        # строка в которой хранятся все ошибки валидации данных при регистрации
        self.validation_errors = ""


    def get(self, request, *args, **kwargs):
        # подмена формы авторизации на регистрационную происходит при добавлении параметра гет запроса
        if (request.GET.get("form") == "reg"):
            self.form_class = RegForm

        # проверка авторизовался ли пользователь
        if (request.GET.get("is_auth") == "false"):
            self.invalid_auth_data = True

        # получение ошибок валидации из параметра гет запроса, этот гет запрос происходит при редиректе из Reg или Auth класса
        # (в зависимости от текущей формы)
        self.validation_errors = request.GET.get("form_errors")

        self.object = None
        return super().get(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (self.invalid_auth_data):
            context[ "auth_error" ] = "Неверный номер телефона или пароль"

        # form_action вставляется в тег form в атрибут action чтобы понимать куда в какую вьюху будет поступать post запрос
        if (self.form_class == AuthForm):
            context[ "form_action" ] = "auth"
        else:
            context[ "form_action" ] = "reg"

        # валидационные ошибки передаются в параметре get запроса в виде строки, ниже логика ее распаршивания
        if (self.validation_errors is not None):
            context[ "validation_errors" ] = self.validation_errors.split(";")

        # context[ goods ] содержит в себе Products.objects.all()
        context[ "products" ] = context[ "goods" ]

        return context


# Класс который содержит в себе форму оформления заказа и логику этого процесса
class OrderPage(BaseView, FormView):
    def __init__(self):
        self.template_name = "core/order.html"
        self.form_class = OrderForm
        self.success_url = reverse_lazy("index")


    def get(self, request, *args, **kwargs):
        # !!!должно быть: or "city" not in request.COOKIES!!!
        # если юзер не авторизован
        if ("user_id" not in request.session):
            logger.debug("User is not auth or city is not selected")
            return HttpResponseRedirect(reverse_lazy("index"))
        return self.render_to_response(self.get_context_data())



    def post(self, request, *args, **kwargs):
        # !!!это поле должно браться из переменных сессии!!!
        user_city_id = 1

        # поле которое нужно для нахождения точки в которой меньше всех текущих заказов
        min_orders_count = 100

        points = Points.objects.filter(city_id=user_city_id)
        for point in points:
            if (point.current_orders_count < min_orders_count):
                min_orders_count = point.current_orders_count

        for point in points:
            if (point.current_orders_count == min_orders_count):
                # поле хранящее pk точки на которую будет назначаться заказ
                point_pk = point.pk
                # прибавление числа текущих заказов
                Points.objects.filter(pk=point_pk).update(current_orders_count=point.current_orders_count+1)
                break


        logger.debug(f"min_orders_count={min_orders_count}")
        logger.debug(f"point_pk={point_pk}")



        deliveryman = None
        # все доставщики который в ожидании заказа
        deliveries = Deliveries.objects.filter(status="waiting an order")
        for deliver in deliveries:
            # если доставщик не выполнял еще ни одного заказа то он моментально назначается на заказ
            if (deliver.last_completed_order is None):
                deliveryman = deliver.pk

        min_last_completed_order = None
        # если не нашлось доставщика который не выполнял ни одного заказа
        if (deliveryman is None):
            for deliver in deliveries:
                # ниже идет логика поиска доставщика который дольше остальных не выполнял заказы
                if (min_last_completed_order is None):
                    min_last_completed_order = deliver.last_completed_order
                else:
                    if (min_last_completed_order > deliver.last_completed_order):
                        min_last_completed_order = deliver.last_completed_order

        # получение pk назначенного доставщик для добавления его pk при добавлении заказа
        deliveryman = deliveries.filter(last_completed_order=min_last_completed_order)[ 0 ].pk
        logger.debug(f"Deliver: {deliveryman}")


        phone = request.session["phone"]
        Orders(
            phone=phone,
            address=request.POST.get("address"),
            apartment=request.POST.get("apartment"),
            floor=request.POST.get("floor"),
            contactless=True if request.POST.get("contactless") == "on" else False,
            price='1000',
            goods='Goods',
            status="cooking",
            is_delivery=True,
            # точка на которой будет приготовление заказа
            point_pk=point_pk,
            # доставщик
            deliveryman=deliveryman,
        ).save()


        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
