from django.contrib import admin
from .models import *



class ProductsAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "description", "category")
    list_display_links = ("title", "price", "description", "category")
    search_fields = ("title", "price")
    list_filter = ("category", "price")



class PointsAdmin(admin.ModelAdmin):
    list_display = ("city", "address")
    list_display_links = ("city", "address")
    search_fields = ("city", "address")
    list_filter = ("city", "address")


admin.site.register(Products, ProductsAdmin)
admin.site.register(ProductsCategories)
admin.site.register(Points, PointsAdmin)
admin.site.register(Cities)