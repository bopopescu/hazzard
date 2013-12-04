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