from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^join$', views.join),
    url(r'^logout$', views.logout),
    url(r'^create$', views.create),
    url(r'^like/(?P<id>\d+)$', views.addlike),
    url(r'^unlike/(?P<id>\d+)$', views.removelike),
    url(r'^friend/(?P<id>\d+)$', views.addfriend),
    url(r'^unfriend/(?P<id>\d+)$', views.removefriend),
    url(r'^show/(?P<id>\d+)$', views.show),
]