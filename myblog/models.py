from django.db import models

# Create your models here.
class SiteInfo(models.Model):
    title = models.CharField(null=True,blank=True,max_length=50)
    logo = models.ImageField(upload_to='logo/',null=True,blank=True)
    def __str__(self):
        return self.title


#课程分类
class Classes(models.Model):
    text = models.CharField(null=True,blank=True,max_length=50)
    def __str__(self):
        return self.text

#用户
class Userinfo(models.Model):
    nickName = models.CharField(null=True,blank=True,max_length=50)
    headImg = models.ImageField(upload_to='userinfo/',null=True,blank=True,)
    belong = models.ForeignKey(Classes,on_delete=models.SET_NULL,related_name="userinfo_classes",null=True,blank=True)
    def __str__(self):
        return self.nickName