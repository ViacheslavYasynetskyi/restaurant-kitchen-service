from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin1234"
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="cook",
            password="cook1234",
            years_of_experience=5
        )

    def test_driver_license_number_listed(self):
        url = reverse("admin:menu_cook_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)

    def test_driver_detail_license_number_listed(self):
        url = reverse("admin:menu_cook_change", args=[self.cook.pk])
        response = self.client.get(url)

        self.assertContains(response, self.cook.years_of_experience)
