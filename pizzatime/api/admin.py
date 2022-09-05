from django.contrib import admin
from .models import *



class PointsAdmin(admin.ModelAdmin):
    list_display = ("city", "address")
    list_display_links = ("city", "address")
    search_fields = ("city", "address")
    list_filter = ("city", "address")


admin.site.register(Points, PointsAdmin)
admin.site.register(Cities)
