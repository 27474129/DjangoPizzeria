from argon2.exceptions import VerifyMismatchError
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import *

import argon2



class RegPage(CreateView):
    form_class = RegForm
    template_name = "users/reg.html"
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (self.request.method == "POST"):
            if (self.request.POST[ "password" ] != self.request.POST[ "password_repeat" ]):
                context["error"] = "Пароли не совпадают"

        return context


class AuthPage(FormView):
    form_class = AuthForm
    template_name = "core/index.html"
    success_url = reverse_lazy("index")

    def __init__(self):
        self.context = {}

    def post(self, request, *args, **kwargs):
        entered_phone = self.request.POST[ "phone" ]

        entered_password = self.request.POST[ "password" ]
        password_hasher = argon2.PasswordHasher()

        user = Users.objects.filter(phone=entered_phone)
        form = self.get_form()


        if (len(user) != 0):
            try:
                password_hasher.verify(user[ 0 ].password, entered_password)
                # 15 days
                self.request.session.set_expiry(1296000)
                self.request.session[ "user_id" ] = user[ 0 ].phone
                return self.form_valid(form)

            except VerifyMismatchError:
                self.context["error"] = "Неправильный номер телефона или пароль"
        else:
            self.context[ "error" ] = "Неправильный номер телефона или пароль"

        return self.form_invalid(form)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context[ "error" ] = self.context[ "error" ]
        except Exception:
            pass
        return context


class LogoutPage(LogoutView):
    success_url_allowed_hosts = reverse_lazy("index")
