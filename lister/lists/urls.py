from django.conf.urls import url
from django.contrib.auth.views import logout

from . import views

app_name = 'lists'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logout/$', logout, {'next_page':'/lists'}, name='logout'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<list_id>[0-9]+)/$', views.lister, name='lister'),
    url(r'^(?P<list_id>[0-9]+)/(?P<item_id>[0-9]+)/(?P<action>[a-z]+)/vote/$', views.vote, name='vote'),
]
