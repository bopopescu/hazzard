from django.contrib import admin
from app.models import User,Role,Form,FormType,Autherize_order,FileUpload

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Form)
admin.site.register(FormType)
admin.site.register(Autherize_order)
admin.site.register(FileUpload)