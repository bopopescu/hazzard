from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^approvement/$', views.approvement, name='approvement'),
    url(r'^login/$', views.login , name='login'),
    url(r'^logout/$', views.logout , name='logout'),
    url(r'^setup/$', views.setup , name='setup'),
    url(r'^list/$',views.list , name='list'),
    url(r'^create/(?P<formtype_id>\d+)/$', views.create_form, name='form'),
    url(r'^modify/(?P<form_id>\d+)/$', views.modify_form, name='modify'),
    url(r'^extend/(?P<form_id>\d+)/$', views.extend_form, name='extend'),
    url(r'^substitute/(?P<form_id>\d+)/$', views.substitute_form, name='copy'),
    url(r'^form/(?P<form_id>\d+)/approve/$', views.approve_form, name='approve'),
    url(r'^form/(?P<form_id>\d+)/approve/approved/$', views.approved, name='approved'),
    url(r'^form/(?P<form_id>\d+)/approve/reject/$', views.reject, name='reject'),
    url(r'^form/(?P<form_id>\d+)/$', views.form_show, name='show'),
    url(r'^file/(?P<file_id>\d+)/$', views.showfile, name='file'),
    #url(r'^form/(?P<form_id>\d+)/$', views.manage_form, name='submit_form'),
    url(r'^pdf/$',views.pdf_export , name='pdf'),
    url(r'^pdf1/$',views.pdf_hold , name='pdf1'),
    url(r'^pdf2/$',views.pdf_register , name='pdf2'),
    url(r'^pdf3/$',views.pdf_sample_produce , name='pdf3'),
    url(r'^pdf4/$',views.pdf_sample_import , name='pdf4'),
    url(r'^pdf5/$',views.pdf_produce , name='pdf5'),
    url(r'^pdf6/$',views.pdf_import , name='pdf6'),

    url(r'^pdf7/$',views.pdf_hold_extend , name='pdf7'),
    url(r'^pdf8/$',views.pdf_import_extend , name='pdf8'),
    url(r'^pdf9/$',views.pdf_export_extend , name='pdf9'),
    url(r'^pdf10/$',views.pdf_produce_extend , name='pdf10'),
    url(r'^pdf11/$',views.pdf_register_extend , name='pdf11'),

    url(r'^pdf12/$',views.pdf_hold_modify , name='pdf12'),
    url(r'^pdf13/$',views.pdf_produce_modify , name='pdf13'),
    url(r'^pdf14/$',views.pdf_import_modify , name='pdf14'),
    url(r'^pdf15/$',views.pdf_export_modify , name='pdf15'),
    url(r'^pdf16/$',views.pdf_register_modify , name='pdf16'),

    url(r'^pdf17/$',views.pdf_exportEND , name='pdf17'),
    url(r'^pdf18/$',views.pdf_importEND , name='pdf18'),
    url(r'^pdf19/$',views.pdf_produceEND , name='pdf19'),
    url(r'^pdf20/$',views.pdf_holdEND , name='pdf20'),
   

)