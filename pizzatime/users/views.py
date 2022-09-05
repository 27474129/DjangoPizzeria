from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View, FormView
from .validation import Validation
from .models import Users
from .forms import ConfirmPhoneForm
from pizzatime.settings import MAILING_API_BASE_URL, MAILING
from core.views import BaseView


import argon2
import logging
import random
import requests



logger = logging.getLogger("debug")



class Reg(BaseView):
    def __init__(self):
        self.url = f"{reverse_lazy('index')}"


    def post(self, request, *args, **kwargs):
        validation = Validation(
            firstname=request.POST[ "firstname" ],
            secondname=request.POST["secondname"],
            phone=request.POST["phone"],
            password=request.POST["password"],
            password_repeat=request.POST[ "password_repeat" ]
        )
        form_errors = validation.validation_errors

        if len(form_errors) != 0:
            return HttpResponseRedirect(f"{reverse_lazy('index')}?form=reg&form_errors={form_errors}")


        hasher = argon2.PasswordHasher()
        password_hash = hasher.hash(request.POST["password"])
        Users(
            firstname=request.POST["firstname"],
            secondname=request.POST["secondname"],
            phone=request.POST["phone"],
            password=password_hash,
            bonuses=0,
            is_activated=False,
        ).save()

        response = HttpResponseRedirect(reverse_lazy("confirm_phone"))
        response.set_cookie("phone", request.POST[ "phone" ])
        return response





class Auth(BaseView):
    def __init__(self):
        self.url = f"{reverse_lazy('index')}?is_auth=false"


    def post(self, request, *args, **kwargs):
        entered_phone = request.POST["phone"]
        entered_password = request.POST["password"]

        password_hasher = argon2.PasswordHasher()

        user = Users.objects.filter(phone=entered_phone)

        if (len(user) != 0):
            try:
                password_hasher.verify(user[0].password, entered_password)
            except Exception:
                return HttpResponseRedirect(self.url)

            if (not user[0].is_activated):
                raise Exception

            # 15 days
            request.session.set_expiry(1296000)
            request.session["user_id"] = user[0].pk
            request.session[ "phone" ] = user[0].phone
            self.url = f"{reverse_lazy('index')}?is_auth=true"

        return HttpResponseRedirect(self.url)


class LogoutPage(LogoutView):
    pass


class ConfirmPhone(BaseView, FormView):
    def __init__(self):
        self.template_name = "users/confirm_phone.html"
        self.form_class = ConfirmPhoneForm
        self.success_url = reverse_lazy("index")
        self.hasher = argon2.PasswordHasher()

    def get(self, request, *args, **kwargs):
        response = self.render_to_response(self.get_context_data())


        confirmation_code = str(483) # random.randint(10000, 99999)
        confirmation_code_hash = self.hasher.hash(confirmation_code)


        api_request = f"{MAILING_API_BASE_URL}number=+7{request.COOKIES[ 'phone' ]}\
        &sign=SMS Aero&text=Ваш код подтверждения: {confirmation_code}"

        if (MAILING):
            api_response_code = requests.get(api_request).status_code
            if (api_response_code != 200):
                logger.warning(requests.get(api_request).text)

            logger.info("Succesfully sent code")


        else:
            logger.warning("Mailing is off")



        response.set_cookie("confirmation_code", confirmation_code_hash)

        return response


    def post(self, request, *args, **kwargs):
        confirmation_code_hash = request.COOKIES.get("confirmation_code")

        if (self.hasher.verify(confirmation_code_hash, request.POST[ "confirmation_code" ])):
            Users.objects.filter(phone=request.COOKIES.get("phone")).update(is_activated=True)
        else:
            return HttpResponseRedirect(reverse_lazy("confirm_phone"))

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

