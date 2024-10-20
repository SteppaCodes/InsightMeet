from django.test import TestCase
from rest_framework.test import APITestCase
from apps.accounts.models import User
from .models import Insightor
from django.urls import reverse


class ProfileViewTest(APITestCase):
    # def setUp(self):
    #     self.user = User.objects.create(
    #         email="steppa@gmail.com",
    #         password="test",
    #         is_insightor=True
    #     )
        

    def test_create_insightor_automatically(self):
        url = reverse('register-user')
        data={
            "email": "steppa@gmail.com",
            "password":"test",
            "is_insightor": True
        }
        response = self.client.post(url, data, format="json")
        self.assertEquals(Insightor.objects.all().count(), 1)
        self.assertEquals(response.status_code, 201)

