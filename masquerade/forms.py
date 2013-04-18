from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class MaskForm(forms.Form):
    mask_user = forms.CharField(max_length=75, label="Username")

    def clean_mask_user(self):
        username = self.cleaned_data['mask_user']
        try:
            u = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Invalid username")
        return username
