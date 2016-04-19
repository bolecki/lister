from django.conf.urls import url

from . import views

app_name = 'api'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<option>[a-z]+)/random/$', views.random, name='random'),
]
