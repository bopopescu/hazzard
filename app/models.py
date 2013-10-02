from django.db import models

# Create your models here.
class Role(models.Model):
	name = models.CharField(max_length=50)
	
class User(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	role = models.ForeignKey(Role)

class FormType(models.Model):
	name = models.CharField(max_length=50)
	autherize_order = models.ManyToManyField(Role, through='Autherize_order')

class Autherize_order(models.Model):
	role = models.ForeignKey(Role)
	formType = models.ForeignKey(FormType,related_name="formType")
	priority = models.IntegerField()

class Form(models.Model):
	formType = models.ForeignKey(FormType)
	user = models.ForeignKey(User)
	data = models.CharField(max_length=99999)

