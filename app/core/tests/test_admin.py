from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="adm@mail.com",
            password="testpwd"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="usr1@mail.com",
            password="testpwd",
            name="TestUserName"
        )

    def test_user_is_listed(self):
        """
        Test if user exists in listed users
        """
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page_open(self):
        """
        Test that change page is opened with correct status
        """
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_user_create_page(self):
        """
        Test user create page is opened with correct status
        """
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
