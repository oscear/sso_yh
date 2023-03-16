from django.contrib.auth import get_user_model
from rest_framework import serializers

from sso.models import Host, Module

CustomUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id",'username', 'password', 'email', 'userAlias', 'userRoles', 'userGroups', 'param')


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'
        # 设置id不是必填项
        extra_kwargs = {"description": {"required": False, "allow_null": True, "allow_blank":True}}



class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'  # 默认序列化全部
