from django.db import models

from rest_framework.views import APIView
from rest_framework.response import Response


STATUS_CHOICE = ((True,"Active"),
                 (False,"Inactive"))


class Base_model(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True,choices=STATUS_CHOICE)

    class Meta:
        abstract = True


def is_user_owner(request_user, item_user):
    """
    Check if the request user is the owner of the item.
    """
    return request_user == item_user