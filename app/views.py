# Create your views here.
from django.http import HttpResponse
def index(request):
	return HttpResponse("Hello, world. You're at index.")
def login(request):
	return HttpResponse('login')
def list(request):
	return HttpResponse('list')
def form(request):
	return HttpResponse('form')
def submit_handle(request):
	return HttpResponse('submit_officer')
