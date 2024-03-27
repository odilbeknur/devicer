from django.contrib import admin
from .models import Category, Model, Device

# Register your models here.
admin.site.register(Category)
admin.site.register(Model)
admin.site.register(Device)
    