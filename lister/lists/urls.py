from django.conf.urls import url

from . import views

app_name = 'lists'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<item_id>[0-9]+)/(?P<action>[a-z]+)/vote/$', views.vote, name='vote'),
]
