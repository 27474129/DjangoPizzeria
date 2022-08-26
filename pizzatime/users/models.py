from django.db import models


class Users(models.Model):
    firstname = models.CharField(max_length=50, verbose_name="Имя")
    secondname = models.CharField(max_length=50, verbose_name="Фамилия")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    password = models.TextField(verbose_name="Пароль")
    bonuses = models.IntegerField(default=0, verbose_name="Бонусы")

    def __str__(self):
        return self.phone