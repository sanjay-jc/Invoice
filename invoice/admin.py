from django.contrib import admin
from .models import (
    Invoice,
    Invoice_details
)

@admin.register(Invoice)
class Invoice_admin(admin.ModelAdmin):
    list_display = ["date","customer_name"]

@admin.register(Invoice_details)
class Invoice_details_admin(admin.ModelAdmin):
    list_display = ['invoice','description','quantity']
