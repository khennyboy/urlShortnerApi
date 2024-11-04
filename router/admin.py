from django.contrib import admin
from .models import Route

# Register your models here.
@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ['original_url', 'key']