from django import forms
from django.db.models import Q

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

class MaskForm(forms.Form):
    mask_user = forms.CharField(max_length=254, label="Username or Email")

    def clean_mask_user(self):
        query = self.cleaned_data['mask_user']
        try:
            u = User.objects.get(
                Q(username=query) |
                Q(email=query)
            )
            self.user = u
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid username or email")
        return u.username
