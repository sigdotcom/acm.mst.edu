# Django
from django.contrib import admin

# local Django
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
