from django.db import models

# Create your models here.
class Role(models.Model):
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return "Role: "+self.name
	
class User(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	role = models.ForeignKey(Role)
	def __unicode__(self):
		return "User: "+self.username+" Role: "+self.role.name

class FormType(models.Model):
	name = models.CharField(max_length=50)
	autherize_order = models.ManyToManyField(Role, through='Autherize_order')
	autherize_number = models.IntegerField()
	def __unicode__(self):
		return "FormType: "+self.name

class Autherize_order(models.Model):
	role = models.ForeignKey(Role)
	formType = models.ForeignKey(FormType,related_name="formType")
	priority = models.IntegerField()

class Form(models.Model):
	formType = models.ForeignKey(FormType)
	user = models.ForeignKey(User)
	data = models.CharField(max_length=99999)
	status = models.IntegerField()
	date = models.DateTimeField()
	expire = models.DateTimeField(null=True)
	def __unicode__(self):
		return "ID :"+str(self.id)+" Form by "+str(self.user)+" Type: "+str(self.formType)+" status: "+str(self.status)


