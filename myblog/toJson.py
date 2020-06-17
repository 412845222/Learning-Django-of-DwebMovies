from rest_framework import serializers
from myblog.models import Classes,Userinfo

class Classes_data(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Classes
        fields = '__all__'

class Userinfo_data(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Userinfo
        fields = '__all__'