from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import View
from .models import Users
from .validation import Validation
from .models import Users

import argon2




class Reg(View):
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

        Users(
            firstname=request.POST[ "firstname" ],
            secondname=request.POST["secondname"],
            phone=request.POST["phone"],
            password=request.POST["password"],
            bonuses=0,
        ).save()
        return HttpResponseRedirect(reverse_lazy("index"))




class Auth(View):
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

            # 15 days
            request.session.set_expiry(1296000)
            request.session["user_id"] = user[0].pk
            self.url = f"{reverse_lazy('index')}?is_auth=true"

        return HttpResponseRedirect(self.url)



class LogoutPage(LogoutView):
    pass
