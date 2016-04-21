from django.conf.urls import url

from . import views

app_name = 'api'
urlpatterns = [
    url(r'^v1/(?P<list_id>[0-9]+)/$', views.index, name='index'),
    url(r'^v1/(?P<list_id>[0-9]+)/random/$', views.random, name='random'),
    url(r'^v1/(?P<list_id>[0-9]+)/random/(?P<option>[a-z]+)/$', views.random, name='random'),
]
