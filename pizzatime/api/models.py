from django.db import models



class Deliveries(models.Model):
    firstname = models.CharField(max_length=70)
    secondname = models.CharField(max_length=70)
    phone = models.IntegerField()
    status = models.CharField(max_length=70)
    last_completed_order = models.DateTimeField(null=True)
    card_number = models.CharField(max_length=70)
    hours_worked = models.IntegerField()




class Points(models.Model):
    address = models.CharField(max_length=150, verbose_name="Адрес точки")
    city = models.ForeignKey("Cities", on_delete=models.PROTECT, verbose_name="Город")
    current_orders_count = models.IntegerField()

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Точки"
        verbose_name_plural = "Точки"
        ordering = [ "city" ]


class Cities(models.Model):
    name = models.CharField(max_length=50, verbose_name="Город")

    class Meta:
        verbose_name = "Города"
        verbose_name_plural = "Города"