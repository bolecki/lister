from django.conf.urls import url

from . import views

app_name = 'api'
urlpatterns = [
    url(r'^v1/$', views.index, name='index'),
    url(r'^v1/random/(?P<option>[a-z]+)/$', views.random, name='random'),
]
