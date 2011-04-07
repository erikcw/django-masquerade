from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings


class MasqueradeTest(TestCase):
    """
    Tests for django-masquerade
    """

    def setUp(self):
        User.objects.create(username='generic', password='abc123',
          is_staff=False, is_superuser=False)
        User.objects.create(username='super', password='abc123', is_staff=True,
          is_superuser=True)
        User.objects.create(username='staff', password='abc123', is_staff=True,
          is_superuser=False)

    def test_superuser_mask(self):
        settings.MASQUERADE_REQUIRE_SUPERUSER = False
        # log in as superuser

        # hit masquerade form with bad username
        # verify form comes back with error

        # hit masquerade form with generic username
        # verify viewing response as generic user

        # require superuser = true
        # log in as superuser
        # hit masquerade form with generic username
        # verify viewing response as generic user

    def test_staff_mask(self):
        # require superuser = false
        # log in as staff
        # hit masquerade form with generic username
        # verify viewing response as generic user

        # require superuser = true
        # log in as staff
        # verify cannot hit masquerade form

    def test_user_mask(self):
        # log in as generic
        # verify cannot hit masquerade form

    def test_unmask(self):
        # log in as superuser
        # hit masquerade form with generic username
        # verify viewing response as generic user

        # request unmask URL
        # verify viewing page as superuser
