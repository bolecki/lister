from django.conf.urls import url
from django.contrib.auth.views import logout

from . import views

app_name = 'lists'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/$', views.api, name='api'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', logout, {'next_page':'/lists'}, name='logout'),
    url(r'^my-lists/$', views.user_lists, name='user_lists'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<list_id>[0-9]+)/$', views.lister, name='lister'),
    url(r'^part/(?P<list_id>[0-9]+)/$', views.part, name='part'),
    url(r'^(?P<list_id>[0-9]+)/grant/$', views.grant, name='grant'),
    url(r'^(?P<list_id>[0-9]+)/(?P<item_id>[0-9]+)/(?P<action>[a-z]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<list_id>[0-9]+)/(?P<old_index>[0-9]+)/(?P<new_index>[0-9]+)/sort/$', views.sort, name='sort'),
]
