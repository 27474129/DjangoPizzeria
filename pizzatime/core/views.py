from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, FormView
from users.forms import RegForm, AuthForm
from .models import Products, Orders
from .forms import *
from django.http import HttpResponseRedirect

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


    def post(self, request, *args, **kwargs):
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
            paid=False,
            is_delivery=True,
        ).save()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

