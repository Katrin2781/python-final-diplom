from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .models import Shop, User, Category, ProductInfo, Order, OrderItem, Contact, ConfirmEmailToken


# Using the standard RequestFactory API to create a form POST request

class ShopTests(APITestCase):
    def setUp(self):
        user_test1 = User.objects.create_user(id=2,
                                              username='test1',
                                              password='ghdfkl',
                                              email='test@mail.ru')
        user_test1.save()
        self.user_token_t1 = Token.objects.create(user=user_test1)

        Category.objects.create(id=224, name='Смартфоны')

        self.data_contact = {

             "country": "Russian Federation",
             "region": "Astrakhan area",
             "city": "Astrakhan",
             "street": "Lenina",
             "house": "32",
             "structure": "5",
             "building": "-",
             "apartment": "121",
             "phone": "25-64-86",
             "postal_code": "45102",

        }
        Contact.objects.create(id=2,
                              country='RF',
                              region="30",
                              city='Astrakhan',
                              street='Boevay',
                              house='12',
                              structure='2',
                              building='9',
                              apartment='45',
                              phone='45-86-78',
                              postal_code='7895632',
                              user_id=2)

        Order.objects.create(id=2,
                             date='2023-09-03',
                             state='basket',
                             contact_id=2,
                             user_id=2)

    def test_categories_get(self):
        url = "/api/v1/categories"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


    def test_shop_get(self):
        url = "/api/v1/shops/"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_user_contact(self):
        url = "/api/v1/user/contact"
        response = self.client.post(url, self.data_contact, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_valid_user_contact(self):
        url = "/api/v1/user/contact"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user_token_t1))
        response = self.client.post(url, self.data_contact, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)


    def test_user_detal(self):
        url = "/api/v1/user/contact"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_register(self):
        url = '/api/v1/user/register'
        data ={

            "first_name": "Anna",
            "last_name": "Ivanova",
            "email": "ivanovaAV@mail.ru",
            "password": "fjskdjfk",
            "company": "Company1",
            "position": "Position1"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_valid_dalete_orders(self):
        url = "/api/v1/basket"
        data = {
                "items": '2'
              }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.user_token_t1))
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

