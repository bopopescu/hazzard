from django.db import models

# Create your models here.
class Role(models.Model):
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return "Role: "+self.name
	
class User(models.Model):
	username = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	name = models.CharField(max_length=100, null=True)
	surname = models.CharField(max_length=100, null=True)
	email = models.CharField(max_length=200, null=True)
	birth_date = models.IntegerField(null=True)
	birth_month = models.IntegerField(null=True)
	birth_year = models.IntegerField(null=True)
	id_no = models.CharField(max_length=20, null=True)
	phone = models.CharField(max_length=20, null=True)
	address = models.CharField(max_length=500, null=True)
	zip_code = models.CharField(max_length=10, null=True)
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

class FileUpload(models.Model):
	key = models.CharField(max_length=200)
	form = models.ForeignKey(Form) 
	uploadType = models.CharField(max_length=20)
	def __unicode__(self):
		return "ID :"+str(self.id)+" Form "+str(self.form)+" Key: "+str(self.key)+" type: "+str(self.uploadType)




