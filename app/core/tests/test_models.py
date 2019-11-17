from django.test import TestCase
from django.contrib.auth import get_user_model

class TestModels(TestCase):

    def test_create_user_with_email_successful(self):
        """
        Test user with email is created successfully
        """
        test_email = "em1@testdom.com"
        test_password = "testPassword"
        user = get_user_model().objects.create_user(
            email=test_email,
            password=test_password
        )

        self.assertEqual(user.email, test_email)
        self.assertTrue(user.check_password(test_password))

    def test_new_user_successful_email_normalization(self):
        """
        Test that new user email is normalized correctly
        """
        test_email = "em1@TESTDOM.cOm"
        test_password = "testPassword"
        user = get_user_model().objects.create_user(
            email=test_email,
            password=test_password
        )

        self.assertEqual(user.email, test_email.lower())

    def test_if_empty_email_raises_value_error(self):
        empty_email = ""
        test_password = "testPassword"
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(
                email=empty_email,
                password=test_password
            )

    def test_super_user_successful_creation(self):
        test_email = "supuser@testdom.com"
        test_password = "testPassword"
        user = get_user_model().objects.create_superuser(
            email=test_email,
            password=test_password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)