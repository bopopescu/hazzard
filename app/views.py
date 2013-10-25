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
	#if user request form 1 use 1 template
		if(formtype_id == '1'):
			date = timezone.now().date()
			context = {'date':date,'user':user_obj}

			return render(request,'main/register_request_customer.html',context)
	info = '<xml>'
	# DO SOME INFOMATION CONVERT TO XML OR SOMETHING
	for key in request.POST:
		value = request.POST[key]
		info += '<'+key+'>'+value+'</'+key+'>'
	info += '</xml>'
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
		return render(request,'main/modify_register_request_customer.html',context)
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
		return render(request,'main/extend_register_request_customer.html',context)

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
		return render(request,'main/substitute_register_request_customer.html',context)

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
	if(form_obj.formType.name == 'register_request'):
		return render(request,'main/register_view_officer.html',context)
	if(form_obj.formType.name == 'register_modify'):
		return render(request,'main/modify_register_view_officer.html',context)
	if(form_obj.formType.name == 'register_extend'):
		return render(request,'main/extend_register_view_officer.html',context)
	if(form_obj.formType.name == 'register_substitute'):
		return render(request,'main/substitute_register_view_officer.html',context)
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
	form_obj.expire = date.replace(date=date.year + 1)
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
	context = {'message':'Permission Denied','user':user_obj}
	return render(request,'main/message.html',context)
	










def setup(request):
	formt1 = FormType(name='register_request',autherize_number=3)
	formt2 = FormType(name='register_extend',autherize_number=1)
	formt3 = FormType(name='register_modify',autherize_number=1)
	formt4 = FormType(name='register_substitute',autherize_number=1)
	formt1.save()
	formt2.save()
	formt3.save()
	formt4.save()
	role1 = Role(name='officer_hazzard')
	role2 = Role(name='officer_plant')
	role3 = Role(name='officer_produce')
	role4 = Role(name='non_autherize_member')
	role5 = Role(name='autherize_member')
	role3.save()
	role1.save()
	role2.save()
	role4.save()
	role5.save()
	a1 = Autherize_order(role=role1,formType=formt1,priority=0)
	a2 = Autherize_order(role=role2,formType=formt1,priority=1)
	a3 = Autherize_order(role=role3,formType=formt1,priority=2)
	a4 = Autherize_order(role=role1,formType=formt2,priority=0)
	a5 = Autherize_order(role=role1,formType=formt3,priority=0)
	a6 = Autherize_order(role=role1,formType=formt4,priority=0)
	a1.save()
	a2.save()
	a3.save()
	a4.save()
	a5.save()
	a6.save()
	u1 = User(username='hazzard',password=hashlib.sha256('1234').hexdigest(),role=role1)
	u2 = User(username='plant',password=hashlib.sha256('1234').hexdigest(),role=role2)
	u3 = User(username='produce',password=hashlib.sha256('1234').hexdigest(),role=role3)
	u4 = User(username='user',password=hashlib.sha256('1234').hexdigest(),role=role5)
	u1.save()
	u2.save()
	u3.save()
	u4.save()
	return HttpResponse('ok')