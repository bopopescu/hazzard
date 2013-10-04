from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse ,HttpResponseRedirect,Http404
from app.models import Form,User,FormType,Autherize_order,Role
from django.utils import timezone
from django.views.decorators.cache import never_cache

def index(request):
	if('user_id' not in request.session):
		return HttpResponseRedirect("login")
	user_obj = User.objects.get(pk=request.session['user_id'])
	#context ?? 
	context = {'user_obj': user_obj }
	return render(request,'main/index.html',context)

def login(request):
	#index if not login go login
	#if already login
	if(request.method != 'POST'):
		return render(request,"main/login.html")
	try:
		user = User.objects.get(username=request.POST['identity'])
		#if login ok then do some redirect to index
		if(user.password == request.POST['password']):
			if(user.role == Role.objects.get(name='non_autherize_member')):
				context = {'message':"UnAutherize"}
				return render(request,'main/login.html',context)
			request.session['user_id'] = user.id
			return HttpResponseRedirect('..')
	except User.DoesNotExist:
		pass
	
	context = {'message':"Username or Password are incorrect."}
	return render(request,'main/login.html',context)

def logout(request):
	#this should work
	try:
		del request.session['user_id']
	except KeyError:
		pass
	return HttpResponseRedirect("..")

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
		return render(request,'main/registration.html',context)
	if( len(user)!=0 ):
		context = {'message':"Username are already used."}
		return render(request,'main/registration.html',context)
	member = User(username=request.POST['idBox'],password=request.POST['passwordBox'],role=Role.objects.get(name='non_autherize_member'))
	member.save()
	#context did not implements
	return HttpResponseRedirect("/")

def list(request):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	if(user_obj.role.name == 'officer'):
		#DO SOMETHING
		context = 'Officer'
		return render(request,'main/officer_documents.html',context)

	#DO SOMETHING
	form_obj = Form.objects.filter(user=user_obj)
	context = {'forms':form_obj}
	print(form_obj)
	#render list.html
	return render(request,'main/customer_documents.html',context)

def create_form(request,formtype_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	if(request.method != 'POST'):
	#if user request form 1 use 1 template
		if(form_id == '1'):
			context = {}
			return render(request,'main/register_request_customer.html',context)
	# DO SOME INFOMATION CONVERT TO XML OR SOMETHING
	info = ''
	formType_obj = FormType.objects.get(pk=form_id)
	form = Form(user=user_obj,formType=formType_obj,data=info,status=0)
	form.save()
	print(form)
	### and other form
	return HttpResponseRedirect('/list')
def edit_form(request,form_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	form_obj = Form.objects.get(pk=form_id)
	if(form.user != user_obj):
		return HttpResponseRedirect("/")
	context = {'form':form_obj}
	return render(request,'main/modify_register_request_customer.html',context)

def extend_form(request,form_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	form_obj = Form.objects.get(pk=form_id)
	if(form.user != user_obj):
		return HttpResponseRedirect("/")
	context = {'form':form_obj}
	return render(request,'main/extend_register_request_customer.html',context)

def approve_form(request,form_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	if(user_obj.role.name != 'officer'):
		return HttpResponseRedirect("/")
	form_obj = Form.objects.get(pk=form_id)


def form_permit_show(request,form_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	if(user_obj.role.name != 'officer'):
		raise PermissionDenied
	return render(request,'main/form_permit_show.html',context)

def form_checking(request):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	#not officer
	if(user_obj.role.name != 'officer'):
		raise PermissionDenied
	#do some get form 
	form_obj = Form.objects.get(pk=request.POST['form_id'])
	#get some info in form obj to context
	return render(request,'main/form_checking.html',context)

def submit_form_checking(request):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	#not officer
	if(user_obj.role.name != 'officer'):
		raise PermissionDenied
	form_obj = Form.objects.get_object_or_404(pk=request.POST['form_id'])
	if(request.POST['approve'] == 'true'):
		form_obj.status += 1
		return HttpResponseRedirect('/list')
	if(request.POST['approve'] == 'false'):
		form_obj.status = -1
		return HttpResponseRedirect('/list')

