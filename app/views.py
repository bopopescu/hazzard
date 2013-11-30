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

### pdf import ###
def pdf_import(request,form_id):

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
    response['Content-Disposition'] = 'attachment; filename="import.pdf"'

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
    p.drawImage(ImageReader("image/permit_import.jpg"), 0, 0, width=595, height=842)
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
        p.drawString(264, 459, data['canton_contactBox'])  #
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
        p.drawString(225, 394, data['hazardous_nameBox'])  #
    elif( data['hazardous_nameBox']  ==  None):
        p.drawString(225, 394, u"")  #
   
    if( data['formulaBox']  !=  None):
        p.drawString(225, 347, data['formulaBox'])  #
    elif( data['formulaBox']  ==  None):
        p.drawString(225, 347, u"")  #

    if( data['marketingBox']  !=  None):
        p.drawString(225, 332, data['marketingBox'])  #
    elif( data['marketingBox']  ==  None):
        p.drawString(225, 332, u"")  #

    if( data['producerBox']  !=  None):
        p.drawString(225, 316, data['producerBox'])  #
    elif( data['producerBox']  ==  None):
        p.drawString(225, 316, u"")  #

    if( data['countryBox']  !=  None):
        p.drawString(225, 299, data['countryBox'])  #
    elif( data['countryBox']  ==  None):
        p.drawString(225, 299, u"")  #

    if( data['quantityBox']  !=  None):
        p.drawString(225, 283, data['quantityBox'])  #
    elif( data['quantityBox']  ==  None):
        p.drawString(225, 283, u"")  #

    if( data['notationBox']  !=  None):
        p.drawString(219, 267, data['notationBox'])  #
    elif( data['notationBox']  ==  None):
        p.drawString(219, 267, u"")  #


    p.drawString(219, 190, u"c")  #
    p.drawString(284, 190, u"d")  #
    p.drawString(355, 190, u"e")  #


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

### pdf export ###
def pdf_export(request,form_id):
    # Create the HttpResponse object with the appropriate PDF headers.

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



    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="export.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()


    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']

    # context = {'form':form_obj,'data':data,'user':user_obj}

    p.setFont('THSarabunNew',16)


    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
   	## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_export.jpg"), 0, 0, width=595, height=842)
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
        p.drawString(225, 394, data['hazardous_nameBox'])  #
    elif( data['hazardous_nameBox']  ==  None):
        p.drawString(225, 394, u"")  #
   
    if( data['formulaBox']  !=  None):
        p.drawString(225, 347, data['formulaBox'])  #
    elif( data['formulaBox']  ==  None):
        p.drawString(225, 347, u"")  #

    if( data['marketingBox']  !=  None):
        p.drawString(225, 332, data['marketingBox'])  #
    elif( data['marketingBox']  ==  None):
        p.drawString(225, 332, u"")  #

    if( data['countryBox']  !=  None):
        p.drawString(225, 316, data['countryBox'])  #
    elif( data['countryBox']  ==  None):
        p.drawString(225, 316, u"")  #

    if( data['quantityBox']  !=  None):
        p.drawString(225, 299, data['quantityBox'])  #
    elif( data['quantityBox']  ==  None):
        p.drawString(225, 299, u"")  #

    if( data['notationBox']  !=  None):
        p.drawString(225, 283, data['notationBox'])  #
    elif( data['notationBox']  ==  None):
        p.drawString(225, 283, u"")  #

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
###


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

## pdf register###
def pdf_register(request,form_id):

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
    response['Content-Disposition'] = 'attachment; filename="register.pdf"'

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
    p.drawImage(ImageReader("image/permit_register.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##

    p.drawString(126, 574, form_id)  #
    # p.drawString(126, 574, data[''])  #
    p.drawString(391, 574, data['dayBox'])  #
    p.drawString(450, 574, data['monthBox'])  #
    p.drawString(511, 574, data['yearBox'])  #

    # p.drawString(511, 574, u"d")  #
    if( data['nameBox']  !=  None):
        p.drawString(140, 558, data['nameBox'])  #
    elif( data['nameBox']  ==  None):
        p.drawString(140, 558, u"")  #

    if( data['regionBox']  !=  None):
        p.drawString(422, 558, data['regionBox'])  #
    elif( data['regionBox']  ==  None):
        p.drawString(422, 558, u"")  #

    if( data['code_taxBox']  !=  None):
        p.drawString(210, 541, data['code_taxBox'])  #
    elif( data['code_taxBox']  ==  None):
        p.drawString(210, 541, u"")  #

    if( data['address_contactBox']  !=  None):
        p.drawString(135, 510, data['address_contactBox'])  #
    elif( data['address_contactBox']  ==  None):
        p.drawString(135, 510, u"")  #
    
    
    if( data['mo_contactBox']  !=  None):
        p.drawString(183, 510, data['mo_contactBox'])  #
    elif( data['mo_contactBox']  ==  None):
        p.drawString(183, 510, u"")  #

    if( data['soi_contactBox']  !=  None):
        p.drawString(256, 510, data['soi_contactBox'])  #
    elif( data['soi_contactBox']  ==  None):
        p.drawString(256, 510, u"")  #

    if( data['street_contactBox']  !=  None):
        p.drawString(140, 494, data['street_contactBox'])  #
    elif( data['street_contactBox']  ==  None):
        p.drawString(140, 494, u"")  #

    if( data['canton_contactBox']  !=  None):
        p.drawString(278, 494, data['canton_contactBox'])  #
    elif( data['canton_contactBox']  ==  None):
        p.drawString(278, 494, u"")  #

    if( data['district_contactBox']  !=  None):
        p.drawString(448, 494, data['district_contactBox'])  #
    elif( data['district_contactBox']  ==  None):
        p.drawString(448, 494, u"")  #

    if( data['province_contactBox']  !=  None):
        p.drawString(125, 478, data['province_contactBox'])  #
    elif( data['province_contactBox']  ==  None):
        p.drawString(125, 478, u"")  #

    if( data['zip_contactBox']  !=  None):
        p.drawString(282, 478, data['zip_contactBox'])  #
    elif( data['zip_contactBox']  ==  None):
        p.drawString(282, 478, u"")  #
    
    if( data['mobile_contactBox']  !=  None):
        p.drawString(380, 478, data['mobile_contactBox'])  #
    elif( data['mobile_contactBox']  ==  None):
        p.drawString(380, 478, u"")  #
  
    if( data['fax_contactBox']  !=  None):
        p.drawString(449, 478, data['fax_contactBox'])  #
    elif( data['fax_contactBox']  ==  None):
        p.drawString(449, 478, u"")  #

    if( data['typeBox']  !=  None):
        p.drawString(309, 446, data['typeBox'])  #
    elif( data['typeBox']  ==  None):
        p.drawString(309, 446, u"")  #

    if( data['toBox']  !=  None):
        p.drawString(391, 446, data['toBox'])  #
    elif( data['toBox']  ==  None):
        p.drawString(391, 446, u"")  #
    
    if( data['hazardous_nameBox']  !=  None):
        p.drawString(250, 431, data['hazardous_nameBox'])  #
    elif( data['hazardous_nameBox']  ==  None):
        p.drawString(250, 431, u"")  #
    
    if( data['formulaBox']  !=  None):
        p.drawString(334, 414, data['formulaBox'])  #
    elif( data['formulaBox']  ==  None):
        p.drawString(334, 414, u"")  #
  
    if( data['marketingBox']  !=  None):
        p.drawString(228, 394, data['marketingBox'])  #
    elif( data['marketingBox']  ==  None):
        p.drawString(228, 394, u"")  #
    
    if( data['producerBox']  !=  None):
        p.drawString(249, 378, data['producerBox'])  #
    elif( data['producerBox']  ==  None):
        p.drawString(249, 378, u"")  #
   
    if( data['importerBox']  !=  None):
        p.drawString(199, 362, data['importerBox'])  #
    elif( data['importerBox']  ==  None):
        p.drawString(199, 362, u"")  #
    
    if( data['seller_nameBox']  !=  None):
        p.drawString(263, 346, data['seller_nameBox'])  #
    elif( data['seller_nameBox']  ==  None):
        p.drawString(263, 346, u"")  #

    if( data['type_usingBox']  !=  None):
        p.drawString(305, 329, data['type_usingBox'])  #
    elif( data['type_usingBox']  ==  None):
        p.drawString(305, 329, u"")  #
    
    if( data['package_nameBox']  !=  None):
        p.drawString(320, 314, data['package_nameBox'])  #
    elif( data['package_nameBox']  ==  None):
        p.drawString(320, 314, u"")  #


    p.drawString(317, 272, u"date")  #
    p.drawString(392, 272, u"date")  #
    p.drawString(475, 272, u"date")  #


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

## pdf sample produce###
def pdf_sample_produce(request,form_id):

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
    response['Content-Disposition'] = 'attachment; filename="sample_import/produce.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
    ## DRAW BACKGROUND IMAGE ##
    if(data['willing_radioButt'] == "import"):
        p.drawImage(ImageReader("image/permit_sample_import.jpg"), 0, 0, width=595, height=842)
    elif(data['willing_radioButt'] == "produce"):
        p.drawImage(ImageReader("image/permit_sample_produce.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##
    

    p.drawString(140, 558, form_id)  #
    p.drawString(267, 558, data['dayBox'])  #
    p.drawString(338, 558, data['monthBox'])  #
    p.drawString(445, 558, data['yearBox'])  #
    

    if( data['nameBox']  !=  None):
        p.drawString(210, 541, data['nameBox'])  #
    elif( data['nameBox']  ==  None):
        p.drawString(210, 541, u"")  #

    if( data['regionBox']  !=  None):
        p.drawString(452, 541, data['regionBox'])  #
    elif( data['regionBox']  ==  None):
        p.drawString(452, 541, u"")  #

    if( data['code_taxBox']  !=  None):
        p.drawString(242, 524, data['code_taxBox'])  #
    elif( data['code_taxBox']  ==  None):
        p.drawString(242, 524, u"")  #

    if( data['address_contactBox']  !=  None):
        p.drawString(252, 507, data['address_contactBox'])  #
    elif( data['address_contactBox']  ==  None):
        p.drawString(252, 507, u"")  #
    
    
    if( data['mo_contactBox']  !=  None):
        p.drawString(278, 507, data['mo_contactBox'])  #
    elif( data['mo_contactBox']  ==  None):
        p.drawString(278, 507, u"")  #

    if( data['soi_contactBox']  !=  None):
        p.drawString(452, 507, data['soi_contactBox'])  #
    elif( data['soi_contactBox']  ==  None):
        p.drawString(452, 507, u"")  #

    if( data['street_contactBox']  !=  None):
        p.drawString(140, 494, data['street_contactBox'])  #
    elif( data['street_contactBox']  ==  None):
        p.drawString(140, 494, u"")  #

    if( data['canton_contactBox']  !=  None):
        p.drawString(278, 494, data['canton_contactBox'])  #
    elif( data['canton_contactBox']  ==  None):
        p.drawString(278, 494, u"")  #

    if( data['district_contactBox']  !=  None):
        p.drawString(448, 494, data['district_contactBox'])  #
    elif( data['district_contactBox']  ==  None):
        p.drawString(448, 494, u"")  #

    if( data['province_contactBox']  !=  None):
        p.drawString(115, 478, data['province_contactBox'])  #
    elif( data['province_contactBox']  ==  None):
        p.drawString(115, 478, u"")  #

    if( data['zip_contactBox']  !=  None):
        p.drawString(246, 478, data['zip_contactBox'])  #
    elif( data['zip_contactBox']  ==  None):
        p.drawString(246, 478, u"")  #
    
    if( data['mobile_contactBox']  !=  None):
        p.drawString(380, 478, data['mobile_contactBox'])  #
    elif( data['mobile_contactBox']  ==  None):
        p.drawString(380, 478, u"")  #
  
    if( data['fax_contactBox']  !=  None):
        p.drawString(339, 478, data['fax_contactBox'])  #
    elif( data['fax_contactBox']  ==  None):
        p.drawString(339, 478, u"")  #

    if( data['name_storage']  !=  None):
        p.drawString(324, 460, data['name_storage'])  #
    elif( data['name_storage']  ==  None):
        p.drawString(324, 460, u"")  #

    if( data['address_storage']  !=  None):
        p.drawString(134, 443, data['address_storage'])  #
    elif( data['address_storage']  ==  None):
        p.drawString(134, 443, u"")  #
    
    if( data['mo_storage']  !=  None):
        p.drawString(191, 443, data['mo_storage'])  #
    elif( data['mo_storage']  ==  None):
        p.drawString(191, 443, u"")  #
    
    if( data['soi_storage']  !=  None):
        p.drawString(281, 443, data['soi_storage'])  #
    elif( data['soi_storage']  ==  None):
        p.drawString(281, 443, u"")  #

    if( data['street_storage']  !=  None):
        p.drawString(423, 443, data['street_storage'])  #
    elif( data['street_storage']  ==  None):
        p.drawString(423, 443, u"")  #
    
    if( data['canton_storage']  !=  None):
        p.drawString(164, 426, data['canton_storage'])  #
    elif( data['canton_storage']  ==  None):
        p.drawString(164, 426, u"")  #

    if( data['district_storage']  !=  None):
        p.drawString(294, 426, data['district_storage'])  #
    elif( data['district_storage']  ==  None):
        p.drawString(294, 426, u"")  #

    if( data['province_storage']  !=  None):
        p.drawString(428, 426, data['province_storage'])  #
    elif( data['province_storage']  ==  None):
        p.drawString(428, 426, u"")  #


    if( data['zip_storage']  !=  None):
        p.drawString(150, 411, data['zip_storage'])  #
    elif( data['zip_storage']  ==  None):
        p.drawString(150, 411, u"")  #

    if( data['mobile_storage']  !=  None):
        p.drawString(273, 411, data['mobile_storage'])  #
    elif( data['mobile_storage']  ==  None):
        p.drawString(273, 411, u"")  #

    if( data['fax_storage']  !=  None):
        p.drawString(416, 411, data['fax_storage'])  #
    elif( data['fax_storage']  ==  None):
        p.drawString(416, 411, u"")  #

    if( data['hazardous_nameBox']  !=  None):
        p.drawString(249, 378, data['hazardous_nameBox'])  #
    elif( data['hazardous_nameBox']  ==  None):
        p.drawString(249, 378, u"")  #
    
    if( data['formulaBox']  !=  None):
        p.drawString(323, 362, data['formulaBox'])  #
    elif( data['formulaBox']  ==  None):
        p.drawString(323, 362, u"")  #
  
    if( data['marketingBox']  !=  None):
        p.drawString(263, 346, data['marketingBox'])  #
    elif( data['marketingBox']  ==  None):
        p.drawString(263, 346, u"")  #
    
    if( data['producerBox']  !=  None):
        p.drawString(305, 331, data['producerBox'])  #
    elif( data['producerBox']  ==  None):
        p.drawString(305, 331, u"")  #
   
    if( data['importerBox']  !=  None):
        p.drawString(320, 315, data['importerBox'])  #
    elif( data['importerBox']  ==  None):
        p.drawString(320, 315, u"")  #
    
    if( data['quantityBox']  !=  None):
        p.drawString(209, 300, data['quantityBox'])  #
    elif( data['quantityBox']  ==  None):
        p.drawString(209, 300, u"")  #

     

    p.drawString(205, 255, u"date")  #
    p.drawString(269, 255, u"date")  #
    p.drawString(386, 255, u"date")  #


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

## pdf sample import###
def pdf_sample_import(request,form_id):

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
    response['Content-Disposition'] = 'attachment; filename="sample_import.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
   	## DRAW BACKGROUND IMAGE ##
    if(data.willing_radioButt == "import"):
        p.drawImage(ImageReader("image/permit_sample_import.jpg"), 0, 0, width=595, height=842)
    elif(data.willing_radioButt == "produce"):
        p.drawImage(ImageReader("image/permit_sample_produce.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##
    

    p.drawString(140, 558, form_id)  #
    p.drawString(267, 558, data['dayBox'])  #
    p.drawString(338, 558, data['monthBox'])  #
    p.drawString(445, 558, data['yearBox'])  #
    

    if( data['nameBox']  !=  None):
        p.drawString(210, 541, data['nameBox'])  #
    elif( data['nameBox']  ==  None):
        p.drawString(210, 541, u"")  #

    if( data['regionBox']  !=  None):
        p.drawString(452, 541, data['regionBox'])  #
    elif( data['regionBox']  ==  None):
        p.drawString(452, 541, u"")  #

    if( data['code_taxBox']  !=  None):
        p.drawString(242, 524, data['code_taxBox'])  #
    elif( data['code_taxBox']  ==  None):
        p.drawString(242, 524, u"")  #

    if( data['address_contactBox']  !=  None):
        p.drawString(252, 507, data['address_contactBox'])  #
    elif( data['address_contactBox']  ==  None):
        p.drawString(252, 507, u"")  #
    
    
    if( data['mo_contactBox']  !=  None):
        p.drawString(278, 507, data['mo_contactBox'])  #
    elif( data['mo_contactBox']  ==  None):
        p.drawString(278, 507, u"")  #

    if( data['soi_contactBox']  !=  None):
        p.drawString(452, 507, data['soi_contactBox'])  #
    elif( data['soi_contactBox']  ==  None):
        p.drawString(452, 507, u"")  #

    if( data['street_contactBox']  !=  None):
        p.drawString(140, 494, data['street_contactBox'])  #
    elif( data['street_contactBox']  ==  None):
        p.drawString(140, 494, u"")  #

    if( data['canton_contactBox']  !=  None):
        p.drawString(278, 494, data['canton_contactBox'])  #
    elif( data['canton_contactBox']  ==  None):
        p.drawString(278, 494, u"")  #

    if( data['district_contactBox']  !=  None):
        p.drawString(448, 494, data['district_contactBox'])  #
    elif( data['district_contactBox']  ==  None):
        p.drawString(448, 494, u"")  #

    if( data['province_contactBox']  !=  None):
        p.drawString(115, 478, data['province_contactBox'])  #
    elif( data['province_contactBox']  ==  None):
        p.drawString(115, 478, u"")  #

    if( data['zip_contactBox']  !=  None):
        p.drawString(246, 478, data['zip_contactBox'])  #
    elif( data['zip_contactBox']  ==  None):
        p.drawString(246, 478, u"")  #
    
    if( data['mobile_contactBox']  !=  None):
        p.drawString(380, 478, data['mobile_contactBox'])  #
    elif( data['mobile_contactBox']  ==  None):
        p.drawString(380, 478, u"")  #
  
    if( data['fax_contactBox']  !=  None):
        p.drawString(339, 478, data['fax_contactBox'])  #
    elif( data['fax_contactBox']  ==  None):
        p.drawString(339, 478, u"")  #

    if( data['name_storage']  !=  None):
        p.drawString(324, 460, data['name_storage'])  #
    elif( data['name_storage']  ==  None):
        p.drawString(324, 460, u"")  #

    if( data['address_storage']  !=  None):
        p.drawString(134, 443, data['address_storage'])  #
    elif( data['address_storage']  ==  None):
        p.drawString(134, 443, u"")  #
    
    if( data['mo_storage']  !=  None):
        p.drawString(191, 443, data['mo_storage'])  #
    elif( data['mo_storage']  ==  None):
        p.drawString(191, 443, u"")  #
    
    if( data['soi_storage']  !=  None):
        p.drawString(281, 443, data['soi_storage'])  #
    elif( data['soi_storage']  ==  None):
        p.drawString(281, 443, u"")  #

    if( data['street_storage']  !=  None):
        p.drawString(423, 443, data['street_storage'])  #
    elif( data['street_storage']  ==  None):
        p.drawString(423, 443, u"")  #
    
    if( data['canton_storage']  !=  None):
        p.drawString(164, 426, data['canton_storage'])  #
    elif( data['canton_storage']  ==  None):
        p.drawString(164, 426, u"")  #

    if( data['district_storage']  !=  None):
        p.drawString(294, 426, data['district_storage'])  #
    elif( data['district_storage']  ==  None):
        p.drawString(294, 426, u"")  #

    if( data['province_storage']  !=  None):
        p.drawString(428, 426, data['province_storage'])  #
    elif( data['province_storage']  ==  None):
        p.drawString(428, 426, u"")  #


    if( data['zip_storage']  !=  None):
        p.drawString(150, 411, data['zip_storage'])  #
    elif( data['zip_storage']  ==  None):
        p.drawString(150, 411, u"")  #

    if( data['mobile_storage']  !=  None):
        p.drawString(273, 411, data['mobile_storage'])  #
    elif( data['mobile_storage']  ==  None):
        p.drawString(273, 411, u"")  #

    if( data['fax_storage']  !=  None):
        p.drawString(416, 411, data['fax_storage'])  #
    elif( data['fax_storage']  ==  None):
        p.drawString(416, 411, u"")  #

    if( data['hazardous_nameBox']  !=  None):
        p.drawString(249, 378, data['hazardous_nameBox'])  #
    elif( data['hazardous_nameBox']  ==  None):
        p.drawString(249, 378, u"")  #
    
    if( data['formulaBox']  !=  None):
        p.drawString(323, 362, data['formulaBox'])  #
    elif( data['formulaBox']  ==  None):
        p.drawString(323, 362, u"")  #
  
    if( data['marketingBox']  !=  None):
        p.drawString(263, 346, data['marketingBox'])  #
    elif( data['marketingBox']  ==  None):
        p.drawString(263, 346, u"")  #
    
    if( data['producerBox']  !=  None):
        p.drawString(305, 331, data['producerBox'])  #
    elif( data['producerBox']  ==  None):
        p.drawString(305, 331, u"")  #
   
    if( data['importerBox']  !=  None):
        p.drawString(320, 315, data['importerBox'])  #
    elif( data['importerBox']  ==  None):
        p.drawString(320, 315, u"")  #
    
    if( data['quantityBox']  !=  None):
        p.drawString(209, 300, data['quantityBox'])  #
    elif( data['quantityBox']  ==  None):
        p.drawString(209, 300, u"")  #

     

    p.drawString(205, 255, u"date")  #
    p.drawString(269, 255, u"date")  #
    p.drawString(386, 255, u"date")  #


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

## pdf register extend ###
def pdf_register_extend(request,form_id):
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
    response['Content-Disposition'] = 'attachment; filename="register_extend.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
   	## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_register_extend.jpg"), 0, 0, width=595, height=842)
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


## pdf sub register###
def pdf_register_sub(request,form_id):
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
    response['Content-Disposition'] = 'attachment; filename="register_sub.pdf"'

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
    p.drawImage(ImageReader("image/permit_register_sub.jpg"), 0, 0, width=595, height=842)
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

### pdf export extend ###
def pdf_export_extend(request,form_id):
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
    response['Content-Disposition'] = 'attachment; filename="export_extend.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
   	## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_export_extend.jpg"), 0, 0, width=595, height=842)
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

### pdf import extend ###
def pdf_import_extend(request,form_id):
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
    response['Content-Disposition'] = 'attachment; filename="import_extend.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
   	## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_import_extend.jpg"), 0, 0, width=595, height=842)
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

### pdf import modify ###
def pdf_import_modify(request,form_id):
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
    response['Content-Disposition'] = 'attachment; filename="import_modify.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
   	## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_import_modify.jpg"), 0, 0, width=595, height=842)
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

### pdf export modify ###
def pdf_export_modify(request,form_id):
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
    response['Content-Disposition'] = 'attachment; filename="export_modify.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
   	## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_export_modify.jpg"), 0, 0, width=595, height=842)
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

### pdf register modify ###
def pdf_register_modify(request,form_id):
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
    response['Content-Disposition'] = 'attachment; filename="register_modify.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
   	## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_register_modify.jpg"), 0, 0, width=595, height=842)
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

## pdf export end ###
def pdf_exportEND(request,form_id):
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
    response['Content-Disposition'] = 'attachment; filename="export_end.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    p.setFont('THSarabunNew',14)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
   	## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_exportEnd.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##
    p.drawString(290, 740, u"a")  #
    p.drawString(290, 723, u"b")  #


    p.drawString(135, 706, u"c")  #
    p.drawString(214, 706, u"c")  #
    p.drawString(302, 706, u"c")  #
    p.drawString(452, 706, u"c")  #

    p.drawString(160, 689, u"d")  #
    p.drawString(318, 689, u"d")  #
    p.drawString(481, 689, u"d")  #

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

## pdf import end ###
def pdf_importEND(request,form_id):
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
    response['Content-Disposition'] = 'attachment; filename="import_end.pdf"'

    pdfmetrics.registerFont(TTFont('THSarabunNew', './font/THSarabunNew.ttf'))
    addMapping('THSarabunNew', 0, 0, 'THSarabunNew')

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    p.setFont('THSarabunNew',14)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
   	## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_importEnd.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##
    p.drawString(290, 740, u"a")  #
    p.drawString(290, 723, u"b")  #


    p.drawString(135, 706, u"c")  #
    p.drawString(214, 706, u"c")  #
    p.drawString(302, 706, u"c")  #
    p.drawString(452, 706, u"c")  #

    p.drawString(160, 689, u"d")  #
    p.drawString(318, 689, u"d")  #
    p.drawString(481, 689, u"d")  #

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

@never_cache
def index(request):
	if('user_id' not in request.session):
		return HttpResponseRedirect("login")
	user_obj = User.objects.get(pk=request.session['user_id'])
	context = {'user': user_obj }
	return render(request,'main/index.html',context)

@never_cache
def login(request):
	#index if not login go login
	#if already login
	if(request.method != 'POST'):
		return render(request,"main/login.html")
	try:
		user = User.objects.get(username=request.POST['identity'])
		#if login ok then do some redirect to index
		if(user.password == hashlib.sha256(request.POST['password']).hexdigest()):
			if(user.role == Role.objects.get(name='non_autherize_member')):
				context = {'message':"Unautherize user."}
				return render(request,'main/message_error_login.html',context)
			request.session['user_id'] = user.id
			return HttpResponseRedirect('/list')
	except User.DoesNotExist:
		pass
	
	context = {'message':'User or password not found.'}
	return render(request,'main/message_error_login.html',context)

@never_cache
def logout(request):
	#this should work
	try:
		del request.session['user_id']
	except KeyError:
		pass
	return HttpResponseRedirect("/")

@never_cache
def profile(request):
	user_obj = User.objects.get(pk=request.session['user_id'])
	context = {'user': user_obj}
	return render(request, 'main/profile.html', context)

@never_cache
def approvement(request):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	if('officer' not in user_obj.role.name ):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/approvement_message.html',context)

	if(request.method != 'POST'):
		return render(request, 'main/approvement.html')

	id_no = request.POST['nameBox']
	role_obj = Role.objects.get(name='non_autherize_member')
	customer_obj = User.objects.filter(id_no=id_no, role=role_obj)
	if(len(customer_obj) == 0):
		context = {'message':"User with id " + id_no + " not found"}
		return render(request,'main/approvement_message.html',context)

	context = {'user': customer_obj[0]}
	return render(request,'main/user_approve.html',context)

@never_cache
def user_approve(request, user_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	if('officer' not in user_obj.role.name ):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/approvement_message.html',context)

	customer_obj = User.objects.get(id=int(user_id))
	approved_role = Role.objects.get(name='autherize_member')
	customer_obj.role = approved_role
	customer_obj.save()
	context = {'message':"User with id " + customer_obj.id_no + " approved to autherized user"}
	return render(request,'main/approvement_message.html',context)

@never_cache
def reject_user(request, user_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	if('officer' not in user_obj.role.name ):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/approvement_message.html',context)

	context = {'message':"User with id " + customer_obj.id_no + " rejected"}
	return render(request,'main/approvement_message.html',context)

@never_cache
def register(request):
	#all this should work ??
	#if not post render register page
	#if post doing some user saving work
	if(request.method != 'POST'):
		return render(request ,'main/registration.html')
	try:
		user = User.objects.filter(username=request.POST['idBox'])
	except KeyError:
		context = {'message':"Please fill all the field"}
		return render(request,'main/message_error_login.html',context)
	if( len(user)!=0 ):
		context = {'message':"Username are already used."}
		return render(request,'main/message_error_login.html',context)
	member = User(username=request.POST['idBox'],password=hashlib.sha256(request.POST['passwordBox']).hexdigest(),role=Role.objects.get(name='non_autherize_member'),
		name=request.POST['nameBox'],surname=request.POST['surnameBox'],email=request.POST['emailBox'],birth_date=request.POST['birthDayBox'],birth_month=request.POST['birthmonthBox'],
		birth_year=request.POST['birthyearBox'],id_no=request.POST['personBox'],phone=request.POST['telBox'],address=request.POST['addressarea'],zip_code=request.POST['zip'])
	member.save()
	context = {'message':'User is created.'}
	return render(request,'main/message_error_login.html',context)

@never_cache
def list(request):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	if('officer' in user_obj.role.name):
		#DO SOMETHING
		context = 'Officer'
		auth_obj = Autherize_order.objects.filter(role=user_obj.role)
		forms_obj=[]
		for auth in auth_obj:
			form_obj = Form.objects.filter(status=auth.priority, formType=auth.formType)
			form_obj2 = Form.objects.filter(status=auth.formType.autherize_number,formType=auth.formType)
			forms_obj+=form_obj
			forms_obj+=form_obj2
		print(forms_obj)
		context = {'forms': forms_obj,'user':user_obj}
		return render(request,'main/officer_documents.html',context)

	#DO SOMETHING
	form_obj = Form.objects.filter(user=user_obj)

	context = { 'forms':form_obj,'user':user_obj}
	print(form_obj)
	#render list.html
	return render(request,'main/customer_documents.html',context)

@never_cache
def create_form(request,formtype_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	if(request.method != 'POST'):
	#register
		if(formtype_id == '1'):
			date = timezone.now().date()
			context = {'date':date,'user':user_obj}
			return render(request,'main/register_request_customer.html',context)
	#produce
		if(formtype_id == '5'):
			date = timezone.now().date()
			context = {'date':date,'user':user_obj}
			return render(request,'main/produce_request_customer.html',context)
	#import
		if(formtype_id == '9'):
			date = timezone.now().date()
			context = {'date':date, 'user':user_obj}
			return render(request,'main/import_request_customer.html', context)
	#hold
		if(formtype_id == '13'):
			date = timezone.now().date()
			context = {'date':date,'user':user_obj}
			return render(request,'main/hold_request_customer.html', context)
	#export
		if(formtype_id == '17'):
			date = timezone.now().date()	
			context = {'date':date,'user':user_obj}
			return render(request,'main/export_request_customer.html', context)
	#sample
		if(formtype_id == '21'):
			date = timezone.now().date()
			context = {'date':date,'user':user_obj}
			return render(request,'main/sample_produce_import_request_customer.html',context)
	
	info = '<xml>'
	# DO SOME INFOMATION CONVERT TO XML OR SOMETHING
	for key in request.POST:
		value = request.POST[key]
		info += '<'+key+'>'+value+'</'+key+'>'
	info += '</xml>'

	print formtype_id

	formType_obj = FormType.objects.get(pk=formtype_id)
	form = Form(user=user_obj,formType=formType_obj,data=info,status=0,date=timezone.now())
	form.save()
	for key in request.FILES.iterkeys():
		print(key)
		uploadFile(request,form,key)	
	context = {'message':'Form have been Saved.','user':user_obj}
	return render(request,'main/message.html',context)

@never_cache
def modify_form(request,form_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	form_obj = Form.objects.get(pk=form_id)
	
	if(form_obj.user != user_obj):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/message.html',context)
	if(request.method != 'POST'):
		date = timezone.now().date()
		data = xmltodict.parse(form_obj.data)['xml']
		context = {'form':form_obj,'data':data,'date':date,'user':user_obj}
		#register
		if(form_obj.formType.id == 1):
			return render(request,'main/register_modify_request_customer.html',context)
		#produce
		if(form_obj.formType.id == 5):
			return render(request,'main/produce_modify_request_customer.html',context)
		#import
		if(form_obj.formType.id == 9):
			return render(request,'main/import_modify_request_customer.html',context)
		#hold
		if(form_obj.formType.id == 13):
			return render(request,'main/hold_modify_request_customer.html',context)
		#export
		if(form_obj.formType.id == 17):
			return render(request,'main/export_modify_request_customer.html',context)
		
	
	formType_obj = FormType.objects.get(name=request.POST['form_type'])
	info = '<xml>'
	for key in request.POST:
		value = request.POST[key]
		info += '<'+key+'>'+value+'</'+key+'>'
	info += '<form_id>'+form_id+'</form_id>'
	info += '</xml>'
	form = Form(user=user_obj,formType=formType_obj,data=info,status=0,date=timezone.now())
	form.save()
	for key in request.FILES.iterkeys():
		print(key)
		uploadFile(request,form,key)	
	context = {'message':'Form have been Saved.','user':user_obj}
	return render(request,'main/message.html',context)

@never_cache
def extend_form(request,form_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	form_obj = Form.objects.get(pk=form_id)
	if(form_obj.user != user_obj):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/message.html',context)
	if(request.method != 'POST'):
		date = timezone.now().date()
		data = xmltodict.parse(form_obj.data)['xml']
		context = {'form':form_obj,'data':data,'date':date,'user':user_obj}

		#register
		if(form_obj.formType.id == 1):
			return render(request,'main/register_extend_request_customer.html',context)
		#produce
		if(form_obj.formType.id == 5):
			return render(request,'main/produce_extend_request_customer.html',context)
		#import
		if(form_obj.formType.id == 9):
			return render(request,'main/import_extend_request_customer.html',context)
		#hold
		if(form_obj.formType.id == 13):
			return render(request,'main/hold_extend_request_customer.html',context)

	formType_obj = FormType.objects.get(name=request.POST['form_type'])
	info = '<xml>'
	for key in request.POST:
		value = request.POST[key]
		info += '<'+key+'>'+value+'</'+key+'>'
	info += '<form_id>'+form_id+'</form_id>'
	info += '</xml>'
	print(info)
	form = Form(user=user_obj,formType=formType_obj,data=info,status=0,date=timezone.now())
	form.save()
	for key in request.FILES.iterkeys():
		print(key)
		uploadFile(request,form,key)	
	context = {'message':'Form have been Saved.','user':user_obj}
	return render(request,'main/message.html',context)

@never_cache
def substitute_form(request,form_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	form_obj = Form.objects.get(pk=form_id)
	if(form_obj.user != user_obj):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/message.html',context)
	if(request.method != 'POST'):
		date = timezone.now().date()
		data = xmltodict.parse(form_obj.data)['xml']
		context = {'form':form_obj,'data':data,'date':date,'user':user_obj}
		#register
		if(form_obj.formType.id == 1):
			return render(request,'main/register_substitute_request_customer.html',context)
		#produce
		if(form_obj.formType.id == 5):
			return render(request,'main/produce_substitute_request_customer.html',context)
		#import
		if(form_obj.formType.id == 9):
			return render(request,'main/import_substitute_request_customer.html',context)
		#hold
		if(form_obj.formType.id == 13):
			return render(request,'main/hold_substitute_request_customer.html',context)
		#export
		if(form_obj.formType.id == 17):
			return render(request,'main/export_substitute_request_customer.html',context)

	formType_obj = FormType.objects.get(name=request.POST['form_type'])
	info = '<xml>'
	for key in request.POST:
		value = request.POST[key]
		info += '<'+key+'>'+value+'</'+key+'>'
	info += '<form_id>'+form_id+'</form_id>'
	info += '</xml>'
	print(info)
	form = Form(user=user_obj,formType=formType_obj,data=info,status=0,date=timezone.now())
	form.save()
	for key in request.FILES.iterkeys():
		print(key)
		uploadFile(request,form,key)	
	context = {'message':'Form have been saved.','user':user_obj}
	return render(request,'main/message.html',context)


@never_cache
def approve_form(request,form_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	print(user_obj.role.name)
	if('officer' not in user_obj.role.name ):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/message.html',context)
	form_obj = Form.objects.get(pk=form_id)
	autherizeOrder = Autherize_order.objects.get(role=user_obj.role,formType=form_obj.formType)
	if(autherizeOrder.priority != form_obj.status):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/message.html',context)
	print(form_obj.data)
	data = xmltodict.parse(form_obj.data)['xml']
	print(data)
	form_file = FileUpload.objects.filter(form=form_obj)
	file_dict = {}
	for i in form_file:
		file_dict[i.uploadType] = i
	print file_dict
	context = { 'form' : form_obj , 'data' : data ,'user':user_obj , 'file' : file_dict}
	#register
	if(form_obj.formType.name == 'register_request'):
		return render(request,'main/register_view_officer.html',context)
	if(form_obj.formType.name == 'register_modify'):
		return render(request,'main/register_modify_view_officer.html',context)
	if(form_obj.formType.name == 'register_extend'):
		return render(request,'main/register_extend_view_officer.html',context)
	if(form_obj.formType.name == 'register_substitute'):
		return render(request,'main/register_substitute_view_officer.html',context)

	#produce
	if(form_obj.formType.name == 'produce_request'):
		return render(request,'main/produce_view_officer.html',context)
	if(form_obj.formType.name == 'produce_modify'):
		return render(request,'main/produce_modify_view_officer.html',context)
	if(form_obj.formType.name == 'produce_extend'):
		return render(request,'main/produce_extend_view_officer.html',context)
	if(form_obj.formType.name == 'produce_substitute'):
		return render(request,'main/produce_substitute_view_officer.html',context)

	#import
	if(form_obj.formType.name == 'import_request'):
		return render(request,'main/import_view_officer.html',context)
	if(form_obj.formType.name == 'import_modify'):
		return render(request,'main/import_modify_view_officer.html',context)
	if(form_obj.formType.name == 'import_extend'):
		return render(request,'main/import_extend_view_officer.html',context)
	if(form_obj.formType.name == 'import_substitute'):
		return render(request,'main/import_substitute_view_officer.html',context)

	#hold
	if(form_obj.formType.name == 'hold_request'):
		return render(request,'main/hold_view_officer.html',context)
	if(form_obj.formType.name == 'hold_modify'):
		return render(request,'main/hold_modify_view_officer.html',context)
	if(form_obj.formType.name == 'hold_extend'):
		return render(request,'main/hold_extend_view_officer.html',context)
	if(form_obj.formType.name == 'hold_substitute'):
		return render(request,'main/hold_substitute_view_officer.html',context)

	#export
	if(form_obj.formType.name == 'export_request'):
		return render(request,'main/export_view_officer.html',context)
	if(form_obj.formType.name == 'export_modify'):
		return render(request,'main/export_modify_view_officer.html',context)
	if(form_obj.formType.name == 'export_extend'):
		return render(request,'main/export_extend_view_officer.html',context)
	if(form_obj.formType.name == 'export_substitute'):
		return render(request,'main/export_substitute_view_officer.html',context)	

	#sample
	if(form_obj.formType.name == 'sample'):
		return render(request,'main/sample_produce_import_view_officer.html',context) #####
	
	return render(request,'main/register_permit_officer.html',context)

@never_cache	
def approved(request,form_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	if('officer' not in user_obj.role.name):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/message.html',context)
	form_obj = Form.objects.get(pk=form_id)
	autherizeOrder = Autherize_order.objects.get(role=user_obj.role,formType=form_obj.formType)
	if(autherizeOrder.priority != form_obj.status):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/message.html',context)
	form_obj.status += 1
	date = timezone.now()
	form_obj.expire = date.replace(year=date.year + 1)
	form_obj.save()
	context = {'message':'Form approved.','user':user_obj}
	return render(request,'main/message.html',context)

@never_cache
def reject(request,form_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	if('officer' not in user_obj.role.name):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/message.html',context)
	form_obj = Form.objects.get(pk=form_id)
	autherizeOrder = Autherize_order.objects.get(role=user_obj.role,formType=form_obj.formType)
	if(autherizeOrder.priority != form_obj.status):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/message.html',context)
	form_obj.status = -1
	form_obj.save()
	print(form_obj)
	context = {'message':'Form rejected.','user':user_obj}
	return render(request,'main/message.html',context)

@never_cache
def form_show(request,form_id):
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

	data = xmltodict.parse(form_obj.data)['xml']
	#register
	if(form_obj.formType.name == 'register_request'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/register_permit.html',context)
	if(form_obj.formType.name == 'register_extend'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/register_extend_permit.html',context)	
	if(form_obj.formType.name == 'register_modify'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/register_modify_permit.html',context)
	if(form_obj.formType.name == 'register_substitute'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/register_substitute_permit.html',context)

	#produce
	if(form_obj.formType.name == 'produce_request'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/produce_permit_officer.html',context)
	if(form_obj.formType.name == 'produce_extend'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/produce_extend_permit_officer.html',context)	
	if(form_obj.formType.name == 'produce_modify'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/produce_modify_permit_officer.html',context)
	if(form_obj.formType.name == 'produce_substitute'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/produce_substitute_permit_officer.html',context)

	#import
	if(form_obj.formType.name == 'import_request'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/import_permit_officer.html',context)
	if(form_obj.formType.name == 'import_extend'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/import_extend_permit_officer.html',context)	
	if(form_obj.formType.name == 'import_modify'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/import_modify_permit_officer.html',context)
	if(form_obj.formType.name == 'import_substitute'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/import_substitute_permit_officer.html',context)

	#hold
	if(form_obj.formType.name == 'hold_request'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/hold_permit_officer.html',context)
	if(form_obj.formType.name == 'hold_extend'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/hold_extend_permit_officer.html',context)	
	if(form_obj.formType.name == 'hold_modify'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/hold_modify_permit_officer.html',context)
	if(form_obj.formType.name == 'hold_substitute'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/hold_substitute_permit_officer.html',context)

	#export
	if(form_obj.formType.name == 'export_request'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/export_permit_officer.html',context)
	if(form_obj.formType.name == 'export_extend'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/export_extend_permit_officer.html',context)	
	if(form_obj.formType.name == 'export_modify'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/export_modify_permit_officer.html',context)
	if(form_obj.formType.name == 'export_substitute'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/export_substitute_permit_officer.html',context)

	#sample
	if(form_obj.formType.name == 'sample'):
		if(data['willing_radioButt'] == "produce") :
			context = {'form':form_obj,'data':data,'user':user_obj}
			return render(request,'main/sample_produce_permit_officer.html',context)
		elif(data['willing_radioButt'] == "import") :
			context = {'form':form_obj,'data':data,'user':user_obj}
			return render(request,'main/sample_import_permit_officer.html',context)

	context = {'message':'Permission Denied','user':user_obj}
	return render(request,'main/message.html',context)
	


def uploadFile(request,form_obj,uploadType):
	def store_in_s3(filename, content, key):
		conn = S3Connection(settings.ACCESS_KEY, settings.PASS_KEY)
		b = conn.create_bucket("testfileink")
		mime = mimetypes.guess_type(filename)[0]
		k = Key(b)
		k.key = key
		k.set_metadata("Content-Type", mime)
		k.set_contents_from_string(content)
		k.set_acl("private")
		return key
	file = request.FILES[uploadType]
	filename = file.name
	filetemp = filename.split('.')
	filetype = filetemp[len(filetemp)-1]
	key = str(form_obj.id)+'_'+str(form_obj.user.id)+'_'+uploadType+'.'+filetype
	content = file.read()
	k = store_in_s3(filename, content,key)
	p = FileUpload(key=k,form=form_obj,uploadType=uploadType)
	p.save()
	print(p.key)
	return

def showfile(request,file_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	file_obj = FileUpload.objects.get(pk=file_id)
	if(file_obj.form.user != user_obj and 'officer' not in user_obj.role.name ):
		context = {'message':'Permission Denied','user':user_obj}
		return render(request,'main/message.html',context)
	conn = S3Connection(settings.ACCESS_KEY, settings.PASS_KEY)
	url = conn.generate_url(60, 'GET',
                            bucket="testfileink",
                            key=file_obj.key,
                            force_http=True)
	print url
	return HttpResponseRedirect(url)





################################################################################################################
##     _____                                                                  O       O        O         O    ##
##    |     \                                       |                        O      OO       OO        O      ##
##    |     /                                       |                      O    OOO       OOO      OOO        ##
##    |____/   ___      ____        _____           |   ____            O   OO      OOOO       OOOO           ##
##    |     \ |   \  | |  __  |   |   |             |  |    |         O  OO   OOO      OOOOO                  ##
##    |     / |___/  | |    | |___|   |       |     |  |____|        O  OO  OOOOOOO                           ##
##    |____/  |   \  | |____| |   |   |       |_____|  |    |       O OO O                       ENTERPRISE   ##
##                                                                                                            ##
################################################################################################################

## SET UP SCRIPT :: HAZARD WEB APPLICATION
## _____________________________________________________________________________________________________________

def setup(request):
	formts = []
	#register
	formts.append(FormType(name='register_request',autherize_number=3))
	formts.append(FormType(name='register_extend',autherize_number=1))
	formts.append(FormType(name='register_modify',autherize_number=1))
	formts.append(FormType(name='register_substitute',autherize_number=1))
	#produce
	formts.append(FormType(name='produce_request',autherize_number=1))
	formts.append(FormType(name='produce_extend',autherize_number=1))
	formts.append(FormType(name='produce_modify',autherize_number=1))
	formts.append(FormType(name='produce_substitute',autherize_number=1))
	#import
	formts.append(FormType(name='import_request',autherize_number=1))
	formts.append(FormType(name='import_extend',autherize_number=1))
	formts.append(FormType(name='import_modify',autherize_number=1))
	formts.append(FormType(name='import_substitute',autherize_number=1))
	#hold
	formts.append(FormType(name='hold_request',autherize_number=1))
	formts.append(FormType(name='hold_extend',autherize_number=1))
	formts.append(FormType(name='hold_modify',autherize_number=1))
	formts.append(FormType(name='hold_substitute',autherize_number=1))
	#export
	formts.append(FormType(name='export_request',autherize_number=1))
	formts.append(FormType(name='export_extend',autherize_number=1))
	formts.append(FormType(name='export_modify',autherize_number=1))
	formts.append(FormType(name='export_substitute',autherize_number=1))
	#sample
	formts.append(FormType(name='sample',autherize_number=1))

	for form in formts :
		form.save()

	#############################################################################

	roles = []
	roles.append(Role(name='officer_hazzard'))
	roles.append(Role(name='officer_plant'))
	roles.append(Role(name='officer_produce'))
	roles.append(Role(name='non_autherize_member'))
	roles.append(Role(name='autherize_member'))
	
	for role in roles :
		role.save()

	#############################################################################

	#register
	auth_orders = []
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[0],priority=0))
	auth_orders.append(Autherize_order(role=roles[1],formType=formts[0],priority=1))
	auth_orders.append(Autherize_order(role=roles[2],formType=formts[0],priority=2))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[2],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[1],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[3],priority=0))

	#produce
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[4],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[5],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[6],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[7],priority=0))

	#import
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[8],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[9],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[10],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[11],priority=0))

	#hold
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[12],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[13],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[14],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[15],priority=0))

	#export
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[16],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[17],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[18],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[19],priority=0))


	#sample
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[20],priority=0))

	for auth_order in auth_orders :
		auth_order.save()

	#############################################################################

	u1 = User(username='hazzard',password=hashlib.sha256('1234').hexdigest(),role=roles[0])
	u2 = User(username='plant',password=hashlib.sha256('1234').hexdigest(),role=roles[1])
	u3 = User(username='produce',password=hashlib.sha256('1234').hexdigest(),role=roles[2])
	u4 = User(username='user',password=hashlib.sha256('1234').hexdigest(),role=roles[4])
	u1.save()
	u2.save()
	u3.save()
	u4.save()

	return HttpResponse('ok')