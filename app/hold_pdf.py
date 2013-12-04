#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse ,HttpResponseRedirect,Http404
from app.models import Form,User,FormType,Autherize_order,Role,FileUpload
import xmltodict
import hashlib
import boto
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import mimetypes

import Image
from reportlab.lib.utils import ImageReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

## pdf hold###
def pdf_hold(request,form_id):
    if('user_id' not in request.session):
        return HttpResponseRedirect("/")
    user_obj = User.objects.get(pk=request.session['user_id'])
    form_obj = Form.objects.get(pk=form_id)
    if(request.method == "POST"):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    if('officer' not in user_obj.role.name and form_obj.user != user_obj):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    if(form_obj.status != form_obj.formType.autherize_number):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="hold.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
   	## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_hold.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##
    p.drawString(150, 590, form_id)  #ใบเลขที่
    p.drawString(425, 573, u"")  #กรม/สำนักงาน
    p.drawString(425, 555, u"")  #กระทรวง


    p.drawString(340, 538, data['dayBox'])  # วันที่
    p.drawString(416, 538, data['monthBox'])  #
    p.drawString(484, 538, data['yearBox'])  #

    if( data['codeBox']  !=  None):
        p.drawString(244, 525, data['codeBox'])  #
    elif( data['codeBox']  ==  None):
        p.drawString(244, 525, u"")  #
    # else
    # p.drawString(244, 525, u"")  #

    if( data['nameBox']  !=  None):
        p.drawString(158, 508, data['nameBox'])  #
    elif( data['nameBox']  ==  None):
        p.drawString(158, 508, u"")  #

    if( data['regionBox']  !=  None):
        p.drawString(432, 508, data['regionBox'])  #
    elif( data['regionBox']  ==  None):
        p.drawString(432, 508, u"")  #
    
   
    if( data['code_taxBox']  !=  None):
        p.drawString(200, 491, data['code_taxBox'])  #
    elif( data['code_taxBox']  ==  None):
        p.drawString(200, 491, u"")  #

    if( data['address_contactBox']  !=  None):
        p.drawString(275, 474, data['address_contactBox'])  #
    elif( data['address_contactBox']  ==  None):
        p.drawString(275, 474, u"")  #

    if( data['mo_contactBox']  !=  None):
        p.drawString(333, 474, data['mo_contactBox'])  #
    elif( data['mo_contactBox']  ==  None):
        p.drawString(333, 474, u"")  #

    if( data['soi_contactBox']  !=  None):
        p.drawString(420, 474, data['soi_contactBox'])  #
    elif( data['soi_contactBox']  ==  None):
        p.drawString(420, 474, u"")  #

    if( data['street_contactBox']  !=  None):
        p.drawString(112, 459, data['street_contactBox'])  #
    elif( data['street_contactBox']  ==  None):
        p.drawString(112, 459, u"")  ##


    if( data['canton_contactBox']  !=  None):
        p.drawString(265, 459, data['canton_contactBox'])  #
    elif( data['canton_contactBox']  ==  None):
        p.drawString(265, 459, u"")  #

   
    if( data['district_contactBox']  !=  None):
        p.drawString(440, 459, data['district_contactBox'])  #
    elif( data['district_contactBox']  ==  None):
        p.drawString(440, 459, u"")  #
    
    if( data['province_contactBox']  !=  None):
        p.drawString(112, 443, data['province_contactBox'])  #
    elif( data['province_contactBox']  ==  None):
        p.drawString(112, 443, u"")  #

    if( data['zip_contactBox']  !=  None):
        p.drawString(251, 443, data['zip_contactBox'])  #
    elif( data['zip_contactBox']  ==  None):
        p.drawString(251, 443, u"")  #

    if( data['mobile_contactBox']  !=  None):
        p.drawString(362, 443, data['mobile_contactBox'])  #
    elif( data['mobile_contactBox']  ==  None):
        p.drawString(362, 443, u"")  #

    if( data['fax_contactBox']  !=  None):
        p.drawString(112, 427, data['fax_contactBox'])  #
    elif( data['fax_contactBox']  ==  None):
        p.drawString(112, 427, u"")  #


    if( data['name_storage']  !=  None):
        p.drawString(270, 410, data['name_storage'])  #
    elif( data['name_storage']  ==  None):
        p.drawString(270, 410, u"")  #

    if( data['address_storage']  !=  None):
        p.drawString(118, 395, data['address_storage'])  #
    elif( data['address_storage']  ==  None):
        p.drawString(118, 395, u"")  #

    if( data['mo_storage']  !=  None):
        p.drawString(195, 395, data['mo_storage'])  #
    elif( data['mo_storage']  ==  None):
        p.drawString(195, 395, u"")  #

    if( data['soi_storage']  !=  None):
        p.drawString(283, 395, data['soi_storage'])  #
    elif( data['soi_storage']  ==  None):
        p.drawString(283, 395, u"")  #

    if( data['street_storage']  !=  None):
        p.drawString(424, 395, data['street_storage'])  #
    elif( data['street_storage']  ==  None):
        p.drawString(424, 395, u"")  #

    if( data['canton_storage']  !=  None):
        p.drawString(140, 380, data['canton_storage'])  #
    elif( data['canton_storage']  ==  None):
        p.drawString(140, 380, u"")  #

    if( data['district_storage']  !=  None):
        p.drawString(320, 380, data['district_storage'])  #
    elif( data['district_storage']  ==  None):
        p.drawString(320, 380, u"")  #


    if( data['province_storage']  !=  None):
        p.drawString(443, 380, data['province_storage'])  #
    elif( data['province_storage']  ==  None):
        p.drawString(442, 380, u"")  #


    if( data['zip_storage']  !=  None):
        p.drawString(153, 365, data['zip_storage'])  #
    elif( data['zip_storage']  ==  None):
        p.drawString(153, 365, u"")  #

    if( data['mobile_storage']  !=  None):
        p.drawString(278, 365, data['mobile_storage'])  #
    elif( data['mobile_storage']  ==  None):
        p.drawString(278, 365, u"")  #

    if( data['fax_storage']  !=  None):
        p.drawString(419, 365, data['fax_storage'])  #
    elif( data['fax_storage']  ==  None):
        p.drawString(419, 365, u"")  

    if( data['specialistBox']  !=  None):
        p.drawString(131, 303, data['specialistBox'])  #
    elif( data['specialistBox']  ==  None):
        p.drawString(131, 303, u"")  #

    if( data['quantityBox']  !=  None):
        p.drawString(228, 269, data['quantityBox'])  #
    elif( data['quantityBox']  ==  None):
        p.drawString(228, 269, u"")  #

    if( data['maxArea_storage']  !=  None):
        p.drawString(294, 252, data['maxArea_storage'])  #
    elif( data['maxArea_storage']  ==  None):
        p.drawString(294, 252, u"")  #

    if( data['to_storage']  !=  None):
        p.drawString(400, 237, data['to_storage'])  #
    elif( data['to_storage']  ==  None):
        p.drawString(400, 237, u"")  #

    if( data['hazardous_nameBox']  !=  None):
        p.drawString(316, 222, data['hazardous_nameBox'])  #
    elif( data['hazardous_nameBox']  ==  None):
        p.drawString(316, 222, u"")  #

    if( data['marketingBox']  !=  None):
        p.drawString(271, 207, data['marketingBox'])  #
    elif( data['marketingBox']  ==  None):
        p.drawString(271, 207, u"")  #

    if( data['codeBox']  !=  None):
        p.drawString(172, 192, data['codeBox'])  #
    elif( data['codeBox']  ==  None):
        p.drawString(172, 192, u"")  #

    if( data['codeBox']  !=  None):
        p.drawString(172, 192, data['codeBox'])  #
    elif( data['codeBox']  ==  None):
        p.drawString(172, 192, u"")  #



    p.drawString(215, 111, u"d")  #
    p.drawString(280, 111, u"d")  #
    p.drawString(386, 111, u"d")  #
	
	
	
    #
    # p.drawString(255, 374, u"y")  #
    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
###

## pdf hold end ###
def pdf_holdEND(request,form_id):
    if('user_id' not in request.session):
        return HttpResponseRedirect("/")
    user_obj = User.objects.get(pk=request.session['user_id'])
    form_obj = Form.objects.get(pk=form_id)
    if(request.method == "POST"):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    if('officer' not in user_obj.role.name and form_obj.user != user_obj):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    if(form_obj.status != form_obj.formType.autherize_number):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)

    if('user_id' not in request.session):
        return HttpResponseRedirect("/")
    user_obj = User.objects.get(pk=request.session['user_id'])
    form_obj = Form.objects.get(pk=form_id)
    if(request.method == "POST"):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    if('officer' not in user_obj.role.name and form_obj.user != user_obj):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    if(form_obj.status != form_obj.formType.autherize_number):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="hold_end.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']

    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
    ## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_holdEnd.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##
    p.drawString(290, 740, u"a")  #
    p.drawString(290, 723, u"b")  #


  
    p.drawString(214, 706, u"c")  #
   

    
    p.drawString(218, 689, u"d")  #
    
    p.drawString(290, 675, u"e")  #
    

    #
    # p.drawString(255, 374, u"y")  #
    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
###

### pdf hold extend ###
def pdf_hold_extend(request,form_id):

    if('user_id' not in request.session):
        return HttpResponseRedirect("/")
    user_obj = User.objects.get(pk=request.session['user_id'])
    form_obj = Form.objects.get(pk=form_id)
    if(request.method == "POST"):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    if('officer' not in user_obj.role.name and form_obj.user != user_obj):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    if(form_obj.status != form_obj.formType.autherize_number):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="hold_extend.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    

    # Create the PDF object, using the BytesIO object as its "file."
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
    ## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_hold_extend.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##
    p.drawString(406, 755, form_id)  #ใบเลขที่


    p.drawString(115, 660, data['dayBox']) 
    p.drawString(126, 660, u".")  
    p.drawString(130, 660, data['monthBox'])  
    p.drawString(145, 660, u".") 
    p.drawString(150, 660, data['yearBox'])  

    # p.drawString(137, 660, data[monthBox])  
    p.drawString(235, 660, data['dayBox'])  #expire
    p.drawString(247, 660, u".")  
    p.drawString(252, 660, data['monthBox'])  #expire
    p.drawString(267, 660, u".") 
    p.drawString(272, 660, data['yearBox'])  #expire

    p.drawString(367, 660, u"")  #list
    
    


    #
    # p.drawString(255, 374, u"y")  #
    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
###


### pdf hold modify ###
def pdf_hold_modify(request,form_id):

    if('user_id' not in request.session):
        return HttpResponseRedirect("/")
    user_obj = User.objects.get(pk=request.session['user_id'])
    form_obj = Form.objects.get(pk=form_id)
    if(request.method == "POST"):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    if('officer' not in user_obj.role.name and form_obj.user != user_obj):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    if(form_obj.status != form_obj.formType.autherize_number):
        context = {'message':'Permission Denied','user':user_obj}
        return render(request,'main/message.html',context)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="hold_modify.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    

    # Create the PDF object, using the BytesIO object as its "file."
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
    ## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_hold_modify.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##
    p.drawString(466, 755, form_id)  #ใบเลขที่


    
    # p.drawString(137, 660, data[monthBox])  
    # p.drawString(215, 660, data['dayBox'])  #
    p.drawString(230, 660, u".")  
    # p.drawString(235, 660, data['monthBox'])  #
    p.drawString(250, 660, u".") 
    # p.drawString(255, 660, data['yearBox'])  #

    if( data['changeArea'] != None ):
        p.drawString(367, 660, data['changeArea'])  #list
    elif( data['changeArea'] == None ):
        p.drawString(367, 660, u"")  #list
    


    #
    # p.drawString(255, 374, u"y")  #
    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
###