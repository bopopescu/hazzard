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


def count_year(request):

    ##YEAR ( EDIT REQUEST YEAR )
    YEAR = '2013'
    count = 0
    response = HttpResponse(content_type='text/html')
    for f in Form.objects.all():
        data = xmltodict.parse(f.data)['xml']
        if data['yearBox'] == str(YEAR):
            count += 1
    response.write("<html><body>OK count : "+str(count)+"</body></html>")
    return response

def country_list(request):
    countries = []
    response = HttpResponse(content_type='text/html')
    for f in Form.objects.all():
        print f.formType.name
        if 'import' in str(f.formType.name) or 'export' in f.formType.name:
            data = xmltodict.parse(f.data)['xml']
            if 'countryBox' in data:
                countries.append(data['countryBox'])
    print countries
    response.write("<html><body>ok "+str(countries)+"</body></html>")
    return response

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

    date = timezone.now().date()
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
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

   

    p.drawString(219, 145, data['dayBox'])  #
    p.drawString(284, 145, data['monthBox'])  #
    p.drawString(355, 145, str(form_obj.expire.year))  #


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

    date = timezone.now().date()
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
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


    p.drawString(219, 190, data['dayBox'])  #
    p.drawString(284, 190, data['monthBox'])  #
    p.drawString(355, 190, str(form_obj.expire.year))  #


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

    date = timezone.now().date()
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
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
    date = timezone.now().date()
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
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



    p.drawString(215, 111, data['dayBox'])  #
    p.drawString(280, 111, data['monthBox'])  #
    p.drawString(386, 111, str(form_obj.expire.year))  #
    
    
    
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
    date = timezone.now().date()
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
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


    p.drawString(317, 272, data['dayBox'])  #
    p.drawString(392, 272, data['monthBox'])  #
    p.drawString(475, 272, str(form_obj.expire.year))  #


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

    date = timezone.now().date()
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
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

     

    p.drawString(205, 255, data['dayBox'])  #
    p.drawString(269, 255, data['monthBox'])  #
    p.drawString(386, 255, str(form_obj.expire.year))  #


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

    date = timezone.now().date()
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
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

    date = timezone.now().date()
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
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
    p.drawString(272, 660, str(form_obj.expire.year))  #expire

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

    date = timezone.now().date()
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
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
    p.drawString(150, 578, form_id)  #ใบเลขที่
    # p.drawString(425, 573, u"")  #กรม/สำนักงาน
    # p.drawString(425, 555, u"")  #กระทรวง


    p.drawString(340, 538, str(form_obj.expire.day))  # วันที่
    p.drawString(416, 538, str(form_obj.expire.month))  #
    p.drawString(484, 538, str(form_obj.expire.year-1))  #

    # if( data['codeBox']  !=  None):
    #     p.drawString(244, 525, data['codeBox'])  #
    # elif( data['codeBox']  ==  None):
    #     p.drawString(244, 525, u"")  #
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



    p.drawString(215, 111, data['dayBox'])  #
    p.drawString(280, 111, data['monthBox'])  #
    p.drawString(386, 111, str(form_obj.expire.year))  #
    
    
    
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

    date = timezone.now()
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
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
    p.drawString(272, 660, str(form_obj.expire.year))  #expire

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

    date = timezone.now().date()
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()

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
    p.drawString(272, 660, str(form_obj.expire.year))  #expire

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

    date = timezone.now().date()
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
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
    p.drawString(235, 660,  data['dayBox']) #expire
    p.drawString(247, 660, u".")  
    p.drawString(252, 660, data['monthBox'])  #expire
    p.drawString(267, 660, u".") 
    p.drawString(272, 660, str(form_obj.expire.year))  #expire

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

    
    date = timezone.now().date()
    # data = xmltodict.parse(form_obj.data)['xml']
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
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
    p.drawString(272, 660, str(form_obj.expire.year))  #expire

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

    date = timezone.now().date()
    # data = xmltodict.parse(form_obj.data)['xml']
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()

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
    p.drawString(215, 660, str(form_obj.expire.day))  #
    p.drawString(230, 660, u".")  
    p.drawString(235, 660, str(form_obj.expire.month))  #
    p.drawString(250, 660, u".") 
    p.drawString(255, 660, str(form_obj.expire.year-1))  #

    if( data['descriptionBox'] != None ):
        p.drawString(367, 660, data['descriptionBox'])  #list
    elif( data['descriptionBox'] == None ):
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

    date = timezone.now().date()
    # data = xmltodict.parse(form_obj.data)['xml']
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
    ## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_produce_modify.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##
    p.drawString(386, 755, form_id)  #ใบเลขที่


    
    # p.drawString(137, 660, data[monthBox])  
    p.drawString(210, 660, str(form_obj.expire.day))  #
    p.drawString(225, 660, u".")  
    p.drawString(230, 660, str(form_obj.expire.month))  #
    p.drawString(245, 660, u".") 
    p.drawString(250, 660, str(form_obj.expire.year-1))  #

    if( data['descriptionBox'] != None ):
        p.drawString(317, 660, data['descriptionBox'])  #list
    elif( data['descriptionBox'] == None ):
        p.drawString(317, 660, u"")  #list
    


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

    date = timezone.now().date()
    data = xmltodict.parse(form_obj.data)['xml']
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
    ## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_import_modify.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##
    p.drawString(386, 755, form_id)  #ใบเลขที่


    
    # p.drawString(137, 660, data[monthBox])  
    p.drawString(210, 660, str(form_obj.expire.day))  #
    p.drawString(225, 660, u".")  
    p.drawString(230, 660, str(form_obj.expire.month))  #
    p.drawString(245, 660, u".") 
    p.drawString(250, 660, str(form_obj.expire.year-1))  #

    if( data['descriptionBox'] != None ):
        p.drawString(317, 660, data['descriptionBox'])  #list
    elif( data['descriptionBox'] == None ):
        p.drawString(317, 660, u"")  #list
    


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
    p.drawString(386, 755, form_id)  #ใบเลขที่


    
    # p.drawString(137, 660, data[monthBox])  
    p.drawString(210, 660, str(form_obj.expire.day))  #
    p.drawString(225, 660, u".")  
    p.drawString(230, 660, str(form_obj.expire.month))  #
    p.drawString(245, 660, u".") 
    p.drawString(250, 660, str(form_obj.expire.year-1))  #

    if( data['descriptionBox'] != None ):
        p.drawString(317, 660, data['descriptionBox'])  #list
    elif( data['descriptionBox'] == None ):
        p.drawString(317, 660, u"asdd")  #list
    


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

    date = timezone.now().date()
    # data = xmltodict.parse(form_obj.data)['xml']
    form_obj.expire = date.replace(year=date.year + 1)
    form_obj.save()
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    data = xmltodict.parse(form_obj.data)['xml']
    p.setFont('THSarabunNew',16)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
   
    ## DRAW BACKGROUND IMAGE ##
    p.drawImage(ImageReader("image/permit_register_modify.jpg"), 0, 0, width=595, height=842)
    ## DRAW STRINGS ##
    p.drawString(386, 755, form_id)  #ใบเลขที่


    
    # p.drawString(137, 660, data[monthBox])  
    p.drawString(210, 660, str(form_obj.expire.day))  #
    p.drawString(225, 660, u".")  
    p.drawString(230, 660, str(form_obj.expire.month))  #
    p.drawString(245, 660, u".") 
    p.drawString(250, 660, str(form_obj.expire.year-1))  #

    if( data['descriptionBox'] != None ):
        p.drawString(317, 660, data['descriptionBox'])  #list
    elif( data['descriptionBox'] == None ):
        p.drawString(317, 660, u"asdd")  #list
    


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