from django.db import models
from core.utils import (
    Base_model
)

from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()

class Invoice(Base_model):
    date = models.DateField()
    customer_name = models.ForeignKey(User,on_delete=models.CASCADE)
    slug_field = models.SlugField(null=True,blank=True)

    def save(self,*args,**kwargs):
        if self.slug_field is None:
            self.slug_field = str(uuid4())[:15]
        return super().save(*args,**kwargs)

    def __str__(self):
        return str(self.customer_name)


class Invoice_details(Base_model):
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE,related_name="invoice_details")
    description = models.TextField()
    quantity = models.PositiveBigIntegerField()
    unit_price = models.PositiveBigIntegerField()
    price = models.PositiveBigIntegerField()
    slug_field = models.SlugField(null=True,blank=True)

    def save(self,*args,**kwargs):
        if self.slug_field is None:
            self.slug_field = str(uuid4())[:20]
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return str(self.invoice)



