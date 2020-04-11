from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse("recipe:tag-list")


class PublicTagsApiTests(TestCase):
    """Test Tags public API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to retrieve that tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """test the authorised user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@email.com",
            "password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Desert")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_tags_to_specific_user(self):
        user2 = get_user_model().objects.create_user(
            "em@mail.com",
            "password333"
        )
        Tag.objects.create(user=user2, name="Fruity")
        tag = Tag.objects.create(user=self.user, name="Comfort Food")

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)

    def test_create_tag_success(self):
        """Test successful tag creation"""
        payload = {"name": "New Tag"}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload["name"]
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creation of a tag with invalid payload"""
        payload = {"name": ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
