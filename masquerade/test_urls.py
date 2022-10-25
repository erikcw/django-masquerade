from django.conf.urls import include, re_path

from masquerade import urls


urlpatterns = [
    re_path(r'', include(urls)),
]
