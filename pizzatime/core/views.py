from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, FormView
from users.forms import RegForm, AuthForm
from .models import Products





class IndexPage(CreateView, ListView):
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




class Order(FormView):
    template_name = ""