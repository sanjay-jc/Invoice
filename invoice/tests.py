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

        response = self.client.get(self.list_invoice)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data['data']), 2) 

    def test_show_todo_invalid_user(self):
        user1 = User.objects.create_user(username='testuser1@email.com', password='testpassword')
        user2 = User.objects.create_user(username='testuser2@email.com', password='testpassword')

        self.client.force_authenticate(user=user1)

        invoice = Invoice.objects.create(
            date='2023-09-26',
            customer_name=user1,
        )

        invoice_detail = Invoice_details.objects.create(
            invoice=invoice,
            description='this is a test case2',
            price=20,
            unit_price=34,
            quantity=30
        )

        self.client.force_authenticate(user=user2)
        response = self.client.get(self.list_invoice)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class Test_create_todo(APITestCase):

    def setUp(self):
        self.create_url = reverse('create_invoice')
        self.user = User.objects.create_user(username='testuser@email.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.token = Token.objects.create(user = self.user)

    def test_create_todo(self):
        self.valid_invoice_data = {
            'date': '2023-09-27',
            'invoice_details': [
                {
                    "description":"test_detaisl",
                    "unit_price":"30",
                    "quantity":"2",
                    "price":"10"
                }
            ]
            
        }
        response = self.client.post(self.create_url, self.valid_invoice_data, format='json')
  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_todo_missing_fields(self):
        self.valid_todo_data = {
            'date': '2023-09-27',
            'invoice_details': [
                {
                    "description":"test_detaisl",
                    "quantity":"2",
                    "price":"10"
                }
            ]      
        }
        response = self.client.post(self.create_url, self.valid_todo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class Test_delet_todo(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser@email.com', password='testpassword')
        self.other_user = get_user_model().objects.create_user(username='otheruser@email.com', password='otherpassword')
        self.client.force_authenticate(user=self.user)
        self.create_url = reverse('create_invoice')
        self.invoice = Invoice.objects.create(
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
        self.delete_url = reverse('delete_invoice') 


    def test_delete_own_invoice(self):
        # Include the slug in request.data for deletion
        delete_data = {'slug_field': self.invoice.slug_field}

        response = self.client.delete(self.delete_url, data=delete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertFalse(Invoice.objects.filter(slug_field=self.invoice.slug_field).exists())


