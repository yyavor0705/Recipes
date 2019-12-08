from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """
    Test the user API (public)
    """

    def setUp(self):
        self.__client = APIClient()

    def test_valid_user_created_success(self):
        """
        Test that valid user is created successfully
        """
        payload = {
            "email": "test1@email.com",
            "password": "testpassword",
            "name": "TEstName"
        }

        res = self.__client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_existing_user_creation_fails(self):
        """
        Test existing user creation failure
        """
        payload = {
            "email": "yy1@mail.com",
            "password": "somepass"
        }
        r = create_user(**payload)
        res = self.__client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_to_short_password(self):
        """
        Test failure is specified password is to short
        """
        payload = {
            "email": "yyy@maill.com",
            "password": "pw"
        }
        res = self.__client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)
