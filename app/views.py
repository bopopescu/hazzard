from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse ,HttpResponseRedirect,Http404
from app.models import Form,User,FormType,Autherize_order,Role
import xmltodict
import hashlib
from django.utils import timezone
from django.views.decorators.cache import never_cache
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
			return HttpResponseRedirect('..')
	except User.DoesNotExist:
		pass
	
	context = {'message':'User or password not found.'}
	return render(request,'main/message_error_login.html',context)

def logout(request):
	#this should work
	try:
		del request.session['user_id']
	except KeyError:
		pass
	return HttpResponseRedirect("/")

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
	member = User(username=request.POST['idBox'],password=hashlib.sha256(request.POST['passwordBox']).hexdigest(),role=Role.objects.get(name='non_autherize_member'))
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
	#sample
		if(formtype_id == '21'):
			date = timezone.now().date()
			context = {'date':date,'user':user_obj}
			return render(request,'main/sample_produce_import_request_customer.html',context)
	#hold
		if (formtype_id == '13'):
			date = timezone.now().date()
			context = {'date':date,'user':user_obj}
			return render(request,'main/hold_request_customer.html', context)
		
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
		if(form_obj.formtype_id == '1'):
			return render(request,'main/modify_register_request_customer.html',context)
		#hold
		if(form_obj.formtype_id == '13'):
			return render(request,'main/modify_hold_request_customer.html',context)
	
	formType_obj = FormType.objects.get(name=request.POST['form_type'])
	info = '<xml>'
	for key in request.POST:
		value = request.POST[key]
		info += '<'+key+'>'+value+'</'+key+'>'
	info += '<form_id>'+form_id+'</form_id>'
	info += '</xml>'
	form = Form(user=user_obj,formType=formType_obj,data=info,status=0,date=timezone.now())
	form.save()
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
		if(form_obj.formtype_id == '1'):
			return render(request,'main/extend_register_request_customer.html',context)
		#hold#
		if(form_obj.formtype_id == '13'):
			return render(request,'main/extend_hold_request_customer.html',context)

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
		if(form_obj.formtype_id == '1'):
			return render(request,'main/substitute_register_request_customer.html',context)
		#hold
		if(form_obj.formtype_id == '13'):
			return render(request,'main/substitute_hold_request_customer.html',context)

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
	context = { 'form' : form_obj , 'data' : data ,'user':user_obj}
	#register
	if(form_obj.formType.name == 'register_request'):
		return render(request,'main/register_view_officer.html',context)
	if(form_obj.formType.name == 'register_modify'):
		return render(request,'main/modify_register_view_officer.html',context)
	if(form_obj.formType.name == 'register_extend'):
		return render(request,'main/extend_register_view_officer.html',context)
	if(form_obj.formType.name == 'register_substitute'):
		return render(request,'main/substitute_register_view_officer.html',context)

	#hold
	if(form_obj.formType.name == 'hold_request'):
		return render(request,'main/hold_view_officer.html',context)
	if(form_obj.formType.name == 'hold_modify'):
		return render(request,'main/modify_hold_view_officer.html',context)
	if(form_obj.formType.name == 'hold_extend'):
		return render(request,'main/extend_hold_view_officer.html',context)
	if(form_obj.formType.name == 'hold_substitute'):
		return render(request,'main/substitute_hold_view_officer.html',context)

	#sample
	if(form_obj.formType.name == 'sample_produce_import'):
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
		return render(request,'main/extend_register_permit.html',context)	
	if(form_obj.formType.name == 'register_modify'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/modify_register_permit.html',context)
	if(form_obj.formType.name == 'register_substitute'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/substitute_register_permit.html',context)

	#hold
	if(form_obj.formType.name == 'hold_request'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/hold_permit_officer.html',context)
	if(form_obj.formType.name == 'hold_extend'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/extend_hold_permit_officer.html',context)	
	if(form_obj.formType.name == 'hold_modify'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/modify_hold_permit_officer.html',context)
	if(form_obj.formType.name == 'hold_substitute'):
		context = {'form':form_obj,'data':data,'user':user_obj}
		return render(request,'main/substitute_hold_permit_officer.html',context)

	#sample
	if(form_obj.formType.name == 'sample_produce_import'):
		if(data['willing_radioButt'] == "produce") :
			context = {'form':form_obj,'data':data,'user':user_obj}
			return render(request,'main/sample_produce_permit_officer.html',context)
		elif(data['willing_radioButt'] == "import") :
			context = {'form':form_obj,'data':data,'user':user_obj}
			return render(request,'main/sample_import_permit_officer.html',context)		
	context = {'message':'Permission Denied','user':user_obj}
	return render(request,'main/message.html',context)
	






##################################################################################################################
##     _____                                       ___                        O       O        O         O      ##
##    |     \                                       |                        O      OO       OO        O        ##
##    |     /                                       |                      O    OOO       OOO      OOO          ##
##    |____/   ___      ____        _____           |   ____            O   OO      OOOO       OOOO             ##
##    |     \ |   \  | |  __  |   |   |             |  |    |         O  OO   OOO      OOOOO                    ##
##    |     / |___/  | |    | |___|   |       |     |  |____|        O  OO  OOOOOOO                             ##
##    |____/  |   \  | |____| |   |   |       |_____|  |    |       O OO O                         ENTERPRISE   ##
##                                                                                                              ##
##################################################################################################################

## SET UP SCRIPT :: HAZARD WEB APPLICATION
## _______________________________________________________________________________________________________________

def setup(request):
	formts = []
	#register
	formts.append(FormType(name='register_request',autherize_number=3))
	formts.append(FormType(name='register_extend',autherize_number=1))
	formts.append(FormType(name='register_modify',autherize_number=1))
	formts.append(FormType(name='register_substitute',autherize_number=1))
	#produce
	formts.append(FormType(name='produce_request',autherize_number=3))
	formts.append(FormType(name='produce_extend',autherize_number=1))
	formts.append(FormType(name='produce_modify',autherize_number=1))
	formts.append(FormType(name='produce_substitute',autherize_number=1))
	#import
	formts.append(FormType(name='import_request',autherize_number=3))
	formts.append(FormType(name='import_extend',autherize_number=1))
	formts.append(FormType(name='import_modify',autherize_number=1))
	formts.append(FormType(name='import_substitute',autherize_number=1))
	#hold
	formts.append(FormType(name='hold_request',autherize_number=1))
	formts.append(FormType(name='hold_extend',autherize_number=1))
	formts.append(FormType(name='hold_modify',autherize_number=1))
	formts.append(FormType(name='hold_substitute',autherize_number=1))
	#export
	formts.append(FormType(name='export_request',autherize_number=3))
	formts.append(FormType(name='export_extend',autherize_number=1))
	formts.append(FormType(name='export_modify',autherize_number=1))
	formts.append(FormType(name='export_substitute',autherize_number=1))
	#sample
	formts.append(FormType(name='sample_produce_import',autherize_number=1))

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
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[4],priority=0))
	#hold
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[12],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[13],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[14],priority=0))
	auth_orders.append(Autherize_order(role=roles[0],formType=formts[15],priority=0))
	
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