from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BasedAdmin

from core import models

class UserAdmin(BasedAdmin):
    ordering = ['id']
    list_display = ['email', 'username']


admin.site.register(models.User, UserAdmin)
