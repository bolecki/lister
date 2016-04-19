from django.conf.urls import url

from . import views

app_name = 'api'
urlpatterns = [
    url(r'^v1/$', views.index, name='index'),
    url(r'^v1/(?P<option>[a-z]+)/random/$', views.random, name='random'),
]
