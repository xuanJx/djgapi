from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Books)
admin.site.register(models.Chapter)
admin.site.register(models.Author)