from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


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

    def test_user_token_creation(self):
        """
        Test is user token creation works properly
        """
        payload = {
            "email": "testuser@mail.com",
            "password": "1234567"
        }
        create_user(**payload)
        res = self.__client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_token_invalid_user_credentials(self):
        """
        Test that token isn't created in case of invalid user credentials
        """
        test_email = "testuser@mail.com"
        payload = {
            "email": test_email,
            "password": "1234567"
        }
        create_user(**payload)
        res = self.__client.post(TOKEN_URL, {"email": test_email, "password": "wrong"})
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        Test that token isn't created if user doesn't exist
        """
        payload = {
            "email": "testuser@mail.com",
            "password": "1234567"
        }
        res = self.__client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_fields(self):
        """
        Test that email and password fields are required
        """
        res = self.__client.post(TOKEN_URL, {"email": "em", "password": ""})
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
