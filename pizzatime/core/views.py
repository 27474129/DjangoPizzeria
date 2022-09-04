from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, FormView
from users.forms import RegForm, AuthForm
from .models import Products, Orders
from .forms import *
from django.http import HttpResponseRedirect
from api.models import Points

import logging


logger = logging.getLogger("debug")


class BaseView(View):

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as exception:
            logger.error(exception)
            return HttpResponseRedirect(reverse_lazy("index"))



class IndexPage(BaseView, CreateView, ListView):
    def __init__(self):
        self.form_class = AuthForm
        self.template_name = "core/index.html"
        self.model = Products
        self.success_url = reverse_lazy("index")
        self.context_object_name = "goods"

        self.invalid_auth_data = False
        self.validation_errors = ""


    def get(self, request, *args, **kwargs):
        # подмена формы авторизации на регистрационную
        if (request.GET.get("form") == "reg"):
            self.form_class = RegForm

            # проверка авторизовался ли пользователь
        if (request.GET.get("is_auth") == "false"):
            self.invalid_auth_data = True


        self.validation_errors = request.GET.get("form_errors")

        self.object = None
        return super().get(request, *args, **kwargs)




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (self.invalid_auth_data):
            context[ "auth_error" ] = "Неверный номер телефона или пароль"

        if (self.form_class == AuthForm):
            context[ "form_action" ] = "auth"
        else:
            context[ "form_action" ] = "reg"

        if (self.validation_errors is not None):
            context[ "validation_errors" ] = self.validation_errors.split(";")

        context[ "products" ] = context[ "goods" ]

        return context


class OrderPage(BaseView, FormView):
    def __init__(self):
        self.template_name = "core/order.html"
        self.form_class = OrderForm
        self.success_url = reverse_lazy("index")


    def get(self, request, *args, **kwargs):
        # should be: or "city" not in request.COOKIES
        if (not request.session.keys):
            logger.info("User is not auth or city is not selected")
            return HttpResponseRedirect(reverse_lazy("index"))
        return self.render_to_response(self.get_context_data())



    def post(self, request, *args, **kwargs):
        user_city_id = 1
        min_orders_count = 100

        points = Points.objects.filter(city_id=user_city_id)
        for point in points:
            if (point.current_orders_count < min_orders_count):
                min_orders_count = point.current_orders_count

        for point in points:
            if (point.current_orders_count == min_orders_count):
                point_pk = point.pk
                Points.objects.filter(pk=point_pk).update(current_orders_count=point.current_orders_count+1)
                break


        logger.debug(f"min_orders_count={min_orders_count}")
        logger.debug(f"point_pk={point_pk}")



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
            point_pk=point_pk,
        ).save()


        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
