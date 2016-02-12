from django.conf.urls import include, url

from masquerade import urls


urlpatterns = [
    url(r'', include(urls)),
]
