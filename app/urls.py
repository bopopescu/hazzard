from django.conf.urls import patterns, url
from app import views
from app import register_pdf
from app import produce_pdf
from app import import_pdf
from app import export_pdf
from app import hold_pdf
from app import sample_produce_pdf
from app import sample_import_pdf

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
    url(r'^form/(?P<form_id>\d+)/pdf/$', export_pdf.pdf_export, name='pdf'),
    # url(r'^pdf/$',export_pdf.pdf_export , name='pdf'),
    url(r'^form/(?P<form_id>\d+)/pdf1/$',hold_pdf.pdf_hold , name='pdf1'),
    url(r'^form/(?P<form_id>\d+)/pdf2/$',register_pdf.pdf_register , name='pdf2'),
    url(r'^form/(?P<form_id>\d+)/pdf3/$',sample_produce_pdf.pdf_sample_produce , name='pdf3'),
    url(r'^form/(?P<form_id>\d+)/pdf4/$',sample_import_pdf.pdf_sample_import , name='pdf4'),
    url(r'^form/(?P<form_id>\d+)/pdf5/$',produce_pdf.pdf_produce , name='pdf5'),
    url(r'^form/(?P<form_id>\d+)/pdf6/$',import_pdf.pdf_import , name='pdf6'),

    url(r'^form/(?P<form_id>\d+)/pdf7/$',hold_pdf.pdf_hold_extend , name='pdf7'),
    url(r'^form/(?P<form_id>\d+)/pdf8/$',import_pdf.pdf_import_extend , name='pdf8'),
    url(r'^form/(?P<form_id>\d+)/pdf9/$',export_pdf.pdf_export_extend , name='pdf9'),
    url(r'^form/(?P<form_id>\d+)/pdf10/$',produce_pdf.pdf_produce_extend , name='pdf10'),
    url(r'^form/(?P<form_id>\d+)/pdf11/$',register_pdf.pdf_register_extend , name='pdf11'),

    url(r'^form/(?P<form_id>\d+)/pdf12/$',hold_pdf.pdf_hold_modify , name='pdf12'),
    url(r'^form/(?P<form_id>\d+)/pdf13/$',produce_pdf.pdf_produce_modify , name='pdf13'),
    url(r'^form/(?P<form_id>\d+)/pdf14/$',import_pdf.pdf_import_modify , name='pdf14'),
    url(r'^form/(?P<form_id>\d+)/pdf15/$',export_pdf.pdf_export_modify , name='pdf15'),
    url(r'^form/(?P<form_id>\d+)/pdf16/$',register_pdf.pdf_register_modify , name='pdf16'),

    url(r'^pdf17/$',export_pdf.pdf_exportEND , name='pdf17'),
    url(r'^pdf18/$',import_pdf.pdf_importEND , name='pdf18'),
    url(r'^pdf19/$',produce_pdf.pdf_produceEND , name='pdf19'),
    url(r'^pdf20/$',hold_pdf.pdf_holdEND , name='pdf20'),
    
    url(r'^form/(?P<form_id>\d+)/pdf21/$',register_pdf.pdf_register_sub , name='pdf21'),   

)