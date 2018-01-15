try:
    from django.conf.urls import url
except ImportError:
    from django.core.urlresolvers import reverse

from masquerade.views import mask, unmask

urlpatterns = [
    url(r'^mask/$', mask, name='masquerade-mask'),
    url(r'^unmask/$', unmask, name='masquerade-unmask'),
]
