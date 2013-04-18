from django.conf import settings
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase, Client
from mock import Mock
from masquerade.middleware import MasqueradeMiddleware
import masquerade.views
import masquerade.signals

class MasqueradeTestCase(TestCase):
    """
    Tests for django-masquerade
    """

    def setUp(self):
        self.mask_on_signal_received = None
        self.mask_off_signal_received = None

        u = User.objects.create_user(username='generic',
          email='generic@foo.com', password='abc123')
        u.is_staff = False
        u.is_superuser = False
        u.save()

        u = User.objects.create_user(username='super',
          email='super@foo.com', password='abc123')
        u.is_staff = True
        u.is_superuser = True
        u.save()

        u = User.objects.create_user(username='staff',
          email='staff@foo.com', password='abc123')
        u.is_staff = True
        u.is_superuser = False
        u.save()

    def test_mask_form_permissions(self):
        settings.MASQUERADE_REQUIRE_SUPERUSER = False

        # log in as superuser
        c = Client()
        self.assert_(c.login(username='super', password='abc123'))

        # hit masquerade form with bad username
        response = c.post(reverse('masquerade.views.mask'), {'mask_user': 'nobody'})

        # verify form comes back with error
        self.assert_(response.status_code == 200)
        self.assert_(response.context['form'].is_valid() == False)

        # hit masquerade form with generic username
        response = c.post(reverse('masquerade.views.mask'),
          {'mask_user': 'generic'})
        self.assert_(response.status_code == 302)

        # make sure non-staff user cannot user form
        c = Client()
        c.login(username='generic', password='abc123')
        response = c.post(reverse('masquerade.views.mask'), {'mask_user': 'nobody'})
        self.assert_(response.status_code == 403)

        # make sure staff user can use form
        c = Client()
        c.login(username='staff', password='abc123')
        response = c.post(reverse('masquerade.views.mask'), {'mask_user': 'nobody'})
        self.assert_(response.status_code == 200)

        # ... unless require superuser setting is true.
        masquerade.views.MASQUERADE_REQUIRE_SUPERUSER = True

        c = Client()
        c.login(username='staff', password='abc123')
        response = c.post(reverse('masquerade.views.mask'), {'mask_user': 'nobody'})
        self.assert_(response.status_code == 403)

    def test_mask(self):
        mw = MasqueradeMiddleware()

        request = Mock(spec=HttpRequest)
        request.session = {'mask_user': 'generic'}
        request.user = User.objects.get(username='super')

        mw.process_request(request)

        self.assert_(request.user.is_masked == True)
        self.assert_(request.user == User.objects.get(username='generic'))

    def test_unmask(self):
        mw = MasqueradeMiddleware()

        request = Mock(spec=HttpRequest)
        request.session = {}
        request.user = User.objects.get(username='super')

        mw.process_request(request)

        self.assert_(request.user.is_masked == False)
        self.assert_(request.user == User.objects.get(username='super'))

    def test_mask_on_signal_sent(self):
        def receiver(sender, mask_username, **kwargs):
            self.mask_on_signal_received = mask_username

        masquerade.signals.mask_on.connect(receiver)
        c = Client()
        c.login(username='super', password='abc123')
        c.post(reverse('masquerade.views.mask'),
          {'mask_user': 'generic'})
        self.assertEqual(self.mask_on_signal_received, 'generic')

    def test_mask_off_signal_sent(self):
        def receiver(sender, mask_username, **kwargs):
            self.mask_off_signal_received = mask_username

        masquerade.signals.mask_off.connect(receiver)
        c = Client()
        c.login(username='super', password='abc123')
        session = c.session
        session['mask_user'] = 'generic'
        session.save()
        c.get(reverse('masquerade.views.unmask'))
        self.assertEqual(self.mask_off_signal_received, 'generic')


