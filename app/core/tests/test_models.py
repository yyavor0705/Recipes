from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email="test@email.com", password="testpwd"):
    """Create sample user"""
    return get_user_model().objects.create_user(email, password)


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
        """
        Test if ValueError is riesd when provided email is empty or None
        """
        empty_email = ""
        test_password = "testPassword"
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(
                email=empty_email,
                password=test_password
            )

    def test_super_user_successful_creation(self):
        """
        Test if super user is created successfuly
        """
        test_email = "supuser@testdom.com"
        test_password = "testPassword"
        user = get_user_model().objects.create_superuser(
            email=test_email,
            password=test_password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test Tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan",
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test Ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Salad",
        )

        self.assertEqual(str(ingredient), ingredient.name)