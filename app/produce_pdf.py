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

### pdf produce###
def pdf_produce(request,form_id):
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
    # data = xmltodict.parse(form_obj.data)['xml']

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="produce.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')


    # data = xmltodict.parse(form_obj.data)['xml']
    #register
    # if(form_obj.formType.name == 'register_request'):
        # context = {'form':form_obj,'data':data,'user':user_obj}
        # return render(request,'main/register_permit.html',context)


    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)


   # if(form_obj.formType.name == 'export_substitute'):
        

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
   	## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_produce.jpg"), 0, 0, width=595, height=842)
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

   
   

    if( data['hazardous_nameBox']  !=  None):
        p.drawString(245, 395, data['hazardous_nameBox'])  #
    elif( data['hazardous_nameBox']  ==  None):
        p.drawString(245, 395, u"")  #
   
    if( data['formulaBox']  !=  None):
        p.drawString(225, 347, data['formulaBox'])  #
    elif( data['formulaBox']  ==  None):
        p.drawString(225, 347, u"")  #

    if( data['marketingBox']  !=  None):
        p.drawString(225, 332, data['marketingBox'])  #
    elif( data['marketingBox']  ==  None):
        p.drawString(225, 332, u"")  #

    if( data['quantityBox']  !=  None):
        p.drawString(225, 316, data['quantityBox'])  #
    elif( data['quantityBox']  ==  None):
        p.drawString(225, 316, u"")  #

    if( data['notationBox']  !=  None):
        p.drawString(225, 299, data['notationBox'])  #
    elif( data['notationBox']  ==  None):
        p.drawString(225, 299, u"")  #


    if( data['specialistBox']  !=  None):
        p.drawString(225, 220, data['specialistBox'])  #
    elif( data['specialistBox']  ==  None):
        p.drawString(225, 220, u"")  #

   

    p.drawString(219, 145, u"c")  #
    p.drawString(284, 145, u"d")  #
    p.drawString(355, 145, u"e")  #


    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
###

## pdf produce end ###
def pdf_produceEND(request,form_id):
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
    response['Content-Disposition'] = 'attachment; filename="produce_end.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    p.setFont('THSarabunNew',14)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
    ## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_produceEnd.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##
    p.drawString(290, 740, u"a")  #
    p.drawString(290, 723, u"b")  #


    p.drawString(135, 706, u"c")  #
    p.drawString(214, 706, u"c")  #
    p.drawString(302, 706, u"c")  #
    p.drawString(452, 706, u"c")  #

    p.drawString(160, 689, u"d")  #
    p.drawString(318, 689, u"d")  #
    p.drawString(458, 689, u"d")  #

    p.drawString(147, 675, u"e")  #
    p.drawString(290, 675, u"e")  #
    p.drawString(461, 675, u"e")  #
   
    p.drawString(138, 612, u"e")  #


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

## pdf produce extend ###
def pdf_produce_extend(request,form_id):
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
    response['Content-Disposition'] = 'attachment; filename="produce_extend.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
    ## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_produce_extend.jpg"), 0, 0, width=595, height=842)
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

### pdf produce modify ###
def pdf_produce_modify(request,form_id):
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
    response['Content-Disposition'] = 'attachment; filename="produce_modify.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
    ## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_produce_modify.jpg"), 0, 0, width=595, height=842)
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