from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login , name='login'),
    url(r'^logout/$', views.logout , name='logout'),
    url(r'^setup/$', views.setup , name='setup'),
    url(r'^list/$',views.list , name='list'),
    url(r'^create/(?P<formtype_id>\d+)/$', views.create_form, name='form'),
    url(r'^modify/(?P<form_id>\d+)/$', views.modify_form, name='modify'),
    url(r'^extend/(?P<form_id>\d+)/$', views.extend_form, name='extend'),
    url(r'^copy/(?P<form_id>\d+)/$', views.copy_form, name='copy'),
    url(r'^form/(?P<form_id>\d+)/approve/$', views.approve_form, name='approve'),
    url(r'^form/(?P<form_id>\d+)/approve/approved/$', views.approved, name='approved'),
    url(r'^form/(?P<form_id>\d+)/approve/reject/$', views.reject, name='reject'),
    url(r'^form/(?P<form_id>\d+)/permit/$', views.form_permit_show, name='permit'),
    url(r'^form/(?P<form_id>\d+)/copy/$', views.copy_form_show, name='copy'),
    #url(r'^form/(?P<form_id>\d+)/$', views.manage_form, name='submit_form'),
)