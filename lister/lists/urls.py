from django.conf.urls import url
from django.contrib.auth.views import logout

from . import views

app_name = 'lists'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<selection>(public|mylists))/$', views.index, name='index'),
    url(r'^api/$', views.api, name='api'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register/(?P<setup>setup)/$', views.register, name='setup'),
    url(r'^logout/$', logout, {'next_page':'/lists'}, name='logout'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<list_id>[0-9]+)/$', views.lister, name='lister'),
    url(r'^index-part/(?P<selection>(public|mylists))/$', views.index_part, name='index_part'),
    url(r'^lister-part/(?P<list_id>[0-9]+)/$', views.lister_part, name='lister_part'),
    url(r'^(?P<list_id>[0-9]+)/grant/$', views.grant, name='grant'),
    url(r'^(?P<list_id>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<list_id>[0-9]+)/clear/$', views.clear, name='clear'),
    url(r'^(?P<list_id>[0-9]+)/(?P<item_id>[0-9]+)/(?P<action>[a-z]+)/vote/$', views.vote, name='vote'),
    url(r'^(?P<list_id>[0-9]+)/(?P<old_index>[0-9]+)/(?P<new_index>[0-9]+)/sort/$', views.sort, name='sort'),
]
