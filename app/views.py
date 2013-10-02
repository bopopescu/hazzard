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
		user = User.objects.get(username=request.POST['username'])
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
		return render(request ,'main/register.html')
	try:
		user = User.objects.filter(username=request.POST['username'])
	except KeyError:
		context = {'message':"Please fill all the field"}
		return render(request,'main/register.html',context)
	if( len(user)!=0 ):
		context = {'message':"Username are already used."}
		return render(request,'main/register.html',context)
	member = User(username=request.POST['username'],password=request.POST['password'],role=Role.objects.get(name='non_autherize_member'))
	member.save()
	return HttpResponseRedirect("/")

def list(request):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	if(user_obj.role.name == 'officer'):
		#DO SOMETHING
		context = 'Officer'
	if(user_obj.role.name == 'autherize_member'):
		#DO SOMETHING
		context = 'Member'
	#render list.html
	return render(request,'main/list.html',context)

def form(request,form_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	#if user request form 1 use 1 template
	if(form_id == '1'):
		context = {}
		return render(request,'main/form1.html',context)
	### and other form
	return HttpResponse('form')

def submit_form(request,form_id):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	# DO SOME INFOMATION CONVERT TO XML OR SOMETHING
	info = ''
	formType_obj = FormType.objects.get(pk=form_id)
	form = Form(user=user_obj,formType=formType_obj,data=info,status=0)
	form.save()
	#show result
	context = {}
	return render(request,'main/result.html',context)

def manage_form(request):
	if('user_id' not in request.session):
		return HttpResponseRedirect("/")
	user_obj = User.objects.get(pk=request.session['user_id'])
	form_obj = Form.objects.filter(user=user_obj)
	context = {}
	return render(request,'main/manage.html',context)
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

