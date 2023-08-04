from django.urls import re_path

from masquerade.views import mask, unmask

urlpatterns = [
    re_path(r"^mask/$", mask, name="masquerade-mask"),
    re_path(r"^unmask/$", unmask, name="masquerade-unmask"),
]
