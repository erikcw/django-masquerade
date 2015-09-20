from django import forms
from django.conf import settings
from django.db.models import Q
from operator import __or__ as OR

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

class MaskForm(forms.Form):
    mask_user = forms.CharField(max_length=254, label="Username or Email")

    def clean_mask_user(self):
        query = self.cleaned_data['mask_user']

        search = [Q(**{f: query}) for f in self.get_user_search_fields()]

        try:
            u = User.objects.get(reduce(OR, search))
            self.user = u
        except User.DoesNotExist:
            raise forms.ValidationError("User not found.")
        return u.username

    def get_user_search_fields(self):
        return getattr(settings, 'MASQUERADE_USER_SEARCH_FIELDS',
                ['username', 'email'])
