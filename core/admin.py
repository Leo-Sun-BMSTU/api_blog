from django.contrib import admin
from core import models


class PostAdmin(admin.ModelAdmin):
    """

    """
    pass


# регистрация модели
admin.site.register(models.Post, PostAdmin)
