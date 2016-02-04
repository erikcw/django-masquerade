from django.conf.urls import patterns, url

from masquerade.views import mask
from masquerade.views import unmask


urlpatterns = [
    url(r'^mask/$', mask),
    url(r'^unmask/$', unmask),
]
