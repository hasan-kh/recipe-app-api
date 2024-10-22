"""Test core API views."""

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


class CoreViewPublicTests(TestCase):
    """Test public core API."""

    def test_health_check_success(self):
        """Test if health_check response is success."""
        client = APIClient()
        url = reverse('health-check')
        res = client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
