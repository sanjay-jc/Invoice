from .views  import (
    List_invoice,
    Create_invoice,
    Update_invoice
)


from django.urls import path


urlpatterns = [
    path('list-invoice',List_invoice.as_view(),name="list_invoice"),
    path('create-invoice',Create_invoice.as_view(),name="create_invoice"),
    path('update-invoice',Update_invoice.as_view(),name="update_invoice"),

    
]