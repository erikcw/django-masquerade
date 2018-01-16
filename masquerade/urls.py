from django.conf.urls import url

from masquerade.views import mask, unmask

urlpatterns = [
    url(r'^mask/$', mask, name='masquerade-mask'),
    url(r'^unmask/$', unmask, name='masquerade-unmask'),
]
