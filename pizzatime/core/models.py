from django.db import models



class Products(models.Model):
    title = models.CharField(max_length=70, verbose_name="Имя товара")
    price = models.IntegerField(verbose_name="Цена")
    description = models.TextField("Описание")
    image = models.TextField("Картинка")
    category = models.ForeignKey("ProductsCategories", on_delete=models.PROTECT, verbose_name="Категория товара")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"
        ordering = ["category"]



class ProductsCategories(models.Model):
    name = models.CharField(max_length=50, verbose_name="Имя категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категории продуктов"
        verbose_name_plural = "Категории продуктов"



class Orders(models.Model):
    phone = models.CharField(max_length=80)
    address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=50)
    floor = models.CharField(max_length=50)
    contactless = models.BooleanField()
    price = models.CharField(max_length=50)
    goods = models.TextField()
    status = models.CharField(max_length=50)
    is_delivery = models.BooleanField()
    point_pk = models.IntegerField(default=0)
