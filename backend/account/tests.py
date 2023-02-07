from django.test import TestCase
from django.urls import reverse

class AccountTestCase(TestCase):
    def setUp(self):
        pass


    def test_create_account(self):
        response = self.client.post(reverse('get_or_create_account'), {'credential': 'whatever'})
        print(response.status_code)
