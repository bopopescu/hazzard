from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login , name='login'),
    url(r'^logout/$', views.logout , name='logout'),
    url(r'^list/$',views.list , name='list'),
    url(r'^create/(?P<formtype_id>\d+)/$', views.create_form, name='form'),
    #url(r'^form/(?P<form_id>\d+)/$', views.manage_form, name='submit_form'),
)