from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Profile)

admin.site.register(models.Deposite)

admin.site.register(models.Withdrawal)