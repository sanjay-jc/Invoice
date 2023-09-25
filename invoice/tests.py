from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient,APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
#local imports

from .models import (
    Invoice,
    Invoice_details
)


User = get_user_model()

class Invoice_test(TestCase):
    ''' to check for creating a todo '''
    def setUp(self):
        self.user = User.objects.create_user(username='tester@username.com', password='adminuser123')
        self.invoice = Invoice.objects.create(
            date='2023-09-26',
            customer_name=self.user,
        )

        self.invoice_details = Invoice_details.objects.create(
            invoice = self.invoice,
            description = 'this is a test case',
            price = 20,
            unit_price = 34,
            quantity = 30
        )

    def test_invoice_creation(self):
        self.assertEqual(self.invoice.date, '2023-09-26')
        self.assertEqual(self.invoice.customer_name, self.user)

    def test_inovice_details(self):
        self.assertEqual(self.invoice_details.invoice, self.invoice)
        self.assertEqual(self.invoice_details.description, 'this is a test case')
        self.assertEqual(self.invoice_details.price,20)
        self.assertEqual(self.invoice_details.unit_price,34)
        self.assertEqual(self.invoice_details.quantity,30)



class List_todo_test(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.token = Token.objects.create(user = self.user)
        self.list_invoice = reverse("list_invoice")

        self.invoice = Invoice.objects.create(
            date='2023-09-26',
            customer_name=self.user,
        )

        self.invoice_details = Invoice_details.objects.create(
            invoice = self.invoice,
            description = 'this is a test case',
            price = 20,
            unit_price = 34,
            quantity = 30
        )

    def test_list_invoice(self):
        Invoice.objects.create(
            date='2023-09-26',
            customer_name=self.user,
        )
        Invoice.objects.create(
            date='2023-09-27',
            customer_name=self.user,
        )
        
        response = self.client.get(self.list_invoice)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['data']), 3) 

    def test_list_invoice_details(self):
        Invoice.objects.create(
            date='2023-09-26',
            customer_name=self.user,
        )
        Invoice_details.objects.create(
            invoice = self.invoice,
            description = 'this is a test case1',
            price = 20,
            unit_price = 34,
            quantity = 30
        )
        Invoice_details.objects.create(
            invoice = self.invoice,
            description = 'this is a test case2',
            price = 20,
            unit_price = 34,
            quantity = 30
        )
        response = self.client.get(self.list_invoice)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['data']), 2) 

    def test_show_todos_with_no_existing_todos(self):
        response = self.client.get(self.list_invoice)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
