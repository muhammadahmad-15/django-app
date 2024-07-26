from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import CustomerSerializer
from .models import Customer
from django.urls import reverse

# Create your tests here.
class CustomerApiTestCase(APITestCase):
    # This method is used to set up any state that you need before running each test.
    # Here, we create a test customer and define valid and invalid payloads for creating and updating a customer.
    def setUp(self):
        self.customer = Customer.objects.create(
            name = "Ahmad",
            email="imats.322@gmail.com",
        )
        self.valid_payload = {
            'name': 'New Customer',
            'email': 'new@example.com',
        }
        self.invalid_payload = {
            'name': '',
            'email': 'invalidemail',
        }
    
    def test_create_customer(self):
        url = reverse("create-customer")
        response = self.client.post(url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_customer(self):
        url = reverse("list-customers")
        response = self.client.get(url, format = 'json')
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many= True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_retrieve_customer(self):
        url = reverse("retrieve-customer", kwargs={'pk': self.customer.pk})
        response = self.client.get(url, format='json')
        customer = Customer.objects.get(pk=self.customer.pk)
        serializer = CustomerSerializer(customer)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
    def test_update_customer(self):
        url = reverse('update-customer', kwargs={'pk': self.customer.pk})
        response = self.client.put(url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, self.valid_payload['name'])
        self.assertEqual(self.customer.email, self.valid_payload['email'])
    
    def test_delete_customer(self):
        url = reverse('delete-customer', kwargs={'pk': self.customer.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Customer.objects.filter(pk=self.customer.pk).exists())
        
    def test_create_customer_invalid(self):
        url = reverse('create-customer')
        response = self.client.post(url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_customer_invalid(self):
        url = reverse("update-customer", kwargs={'pk': self.customer.pk})
        response = self.client.put(url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)