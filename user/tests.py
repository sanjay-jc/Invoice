from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient,APITestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token

User = get_user_model()

class Custom_user_test(TestCase):
    def setUp(self):
        self.user_data = {
            "username":"tester",
            "password":"helloworld",
            "first_name":"Tester"

        }

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.first_name,self.user_data['first_name'])

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(**self.user_data)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)


    def test_user_str_representation(self):
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['username'])




class Registration_test_case(APITestCase):

    def setUp(self):
        self.registration_url = reverse('register')
        self.user_data = {
            "username":"testuser",
            "password":"testuser123"
        }
        self.existing_user_data = {
            "username": "existinguse",
            "password": "existinguser123"
        }
        self.existing_user = get_user_model().objects.create_user(**self.existing_user_data)

    def test_registration(self):
        '''test user registration'''
        response = self.client.post(self.registration_url,self.user_data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)



    def test_registration_existing_user(self):
        '''test user registration with existing details  '''

        response = self.client.post(self.registration_url,self.existing_user_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_registration_missing_fields(self):
        '''test user registration with missing fields '''

        invalid_data = {
            'password': 'short',
        }
        response = self.client.post(self.registration_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)






class User_login_test_case(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'testuser@username.com',
            'password': 'testpassword',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

    def test_user_login(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.token}')
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.client.force_authenticate(user=self.user)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_user_login_invalid(self):
        invalid_user_data = {
            'username': self.user_data['username'],
            'password':'password',
        }

        response = self.client.post(self.login_url,invalid_user_data, format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_user_login_missing_field(self):
        invalid_user_data = {
            'password':'password',
        }

        response = self.client.post(self.login_url,invalid_user_data, format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)