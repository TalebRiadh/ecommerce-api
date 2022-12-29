

from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
from phone_gen import PhoneNumber

from authentication.models import User


class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('authentication:user_register')
        self.login_url = reverse('authentication:user_login')
        self.fake = Faker(locale='fr_FR')
        self.password = self.fake.password(length=12)
        self.user_data = {
            "username": self.fake.email().split('@')[0],
            "email": self.fake.email(),
            "password1": self.password,
            "password2": self.password,
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "phone_number": PhoneNumber("DZ").get_number()
        }

        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()