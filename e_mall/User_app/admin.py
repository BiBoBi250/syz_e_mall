from django.contrib import admin
from .models.user_models import Consumer
# Register your models here.

@admin.register(Consumer)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)