from django.contrib import admin
from myblog.models import SiteInfo,Classes,Userinfo
# Register your models here.
admin.site.register(SiteInfo)
admin.site.register(Classes)
admin.site.register(Userinfo)