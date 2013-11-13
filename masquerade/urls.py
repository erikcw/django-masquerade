from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^mask/$', 'masquerade.views.mask'),
    url(r'^unmask/$', 'masquerade.views.unmask'),
)
