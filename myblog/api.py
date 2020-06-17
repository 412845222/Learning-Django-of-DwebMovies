from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from django.contrib.auth.hashers import check_password,make_password

from myblog.models import Classes,Userinfo,SiteInfo
from myblog.toJson import Classes_data,Userinfo_data
import json
@api_view(['GET','POST'])
def api_test(request):
    classes = Classes.objects.all()
    # classes_data = Classes_data(classes,many=True)
    # userlist = Userinfo.objects.all()
    # userlist_data = Userinfo_data(userlist,many=True)

    # data = {
    #     'classes':classes_data.data,
    #     'userlist':userlist_data.data
    # }

    data = {
        'classes':[]
    }
    for c in classes:
        data_item = {
            'id':c.id,
            'text':c.text,
            'userlist':[]
        }
        userlist = c.userinfo_classes.all()
        for user in userlist:
            user_data = {
                'id':user.id,
                'nickName':user.nickName,
                'headImg':str(user.headImg)
            }
            data_item['userlist'].append(user_data)
        data['classes'].append(data_item)
    return Response(data)

@api_view(['GET'])
def getMenuList(request):
    allClasses = Classes.objects.all()
    siteinfo = SiteInfo.objects.get(id=1)
    siteinfo_data = {
        'sitename':siteinfo.title,
        'logo': 'http://127.0.0.1:9000/upload/'+str(siteinfo.logo)
    }
    #整理数据为json
    menu_data = []
    for c in allClasses:
        #设计单条数据的结构
        data_item = {
            'id':c.id,
            'text':c.text
        }
        menu_data.append(data_item)

    data = {
        'menu_data':menu_data,
        'siteinfo':siteinfo_data
    }
    return Response(data)

@api_view(['GET','DELETE'])
def getUserList(request):
    if request.method == 'DELETE':
        user_id = request.POST['id']
        print(user_id)
        deleteUser = Userinfo.objects.get(id=user_id)
        deleteUser.delete()
        return Response('ok')
    menuId = request.GET['id']
    print(menuId)
    menu = Classes.objects.get(id=menuId)
    print(menu)
    userlist = Userinfo.objects.filter(belong=menu)
    print(userlist)

    #开始整理数据列表
    data = []
    for user in userlist:
        data_item = {
            'id':user.id,
            'headImg':str(user.headImg),
            'nickName':user.nickName
        }
        data.append(data_item)
    return Response(data)

@api_view(['POST'])
def toLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    print(username,password)
    #查询用户数据库
    user = User.objects.filter(username=username)
    if len(user)>0:
        user_pwd = user[0].password
        auth_pwd = check_password(password,user_pwd)
        print(auth_pwd)
        if auth_pwd:
            token = Token.objects.update_or_create(user=user[0])
            token = Token.objects.get(user=user[0])
            print(token.key)
            data = {
                'token':token.key
            }
            return Response(data)
        else:
            return Response('pwderr')
        
    else:
        return Response('none')

@api_view(['GET','POST'])
def toRegister(request):
    username = request.POST['username']
    password = request.POST['password']
    password2 = request.POST['password2']
    print(username,password,password2)
    #用户是否存在
    user = User.objects.filter(username=username)
    if user:
        return Response('same')
    else:
        newPwd = make_password(password,username)
        print(newPwd)
        newUser = User(username=username,password=newPwd)
        newUser.save()
    return Response('ok')

@api_view(['POST','PUT'])
def uploadLogo(request):
    if request.method == "PUT":
        sitename = request.POST['sitename']
        print(sitename)
        old_info = SiteInfo.objects.get(id=1)
        old_info.title = sitename
        new_info = SiteInfo.objects.get(id=2)
        old_info.logo = new_info.logo
        old_info.save()
        return Response('ok')
    img = request.FILES['logo']
    print(img)
    test_siteLogo = SiteInfo.objects.get(id=2)
    test_siteLogo.logo = img
    test_siteLogo.save()
    data = {
        'img':str(test_siteLogo.logo)
    }
    return Response(data)