from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.1
# 项目管理


class CustomUser(AbstractUser):
    userAlias = models.CharField(verbose_name='用户别名', max_length=30, default="")
    userRoles = models.CharField(verbose_name='用户角色', max_length=30, default="")
    userGroups = models.CharField(verbose_name='用户分组', max_length=30, default="")
    param = models.CharField(verbose_name='用户参数', max_length=500, default="", blank=True)


class Module(models.Model):
    index = models.CharField(verbose_name='路径', max_length=30,default="")
    title = models.CharField(verbose_name="标题名", max_length=30,default="")
    url = models.CharField(verbose_name='报告名', max_length=500,default="")
    # created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # # 创建时间
    # modified_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    # 更新时间

    class Meta:
        verbose_name = '模块管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.index


class Host(models.Model):
    '''
    host环境配置
    '''
    name = models.CharField(verbose_name='环境名称', max_length=50)
    version = models.CharField(verbose_name='产品版本', max_length=10, default="")
    host = models.CharField(verbose_name='环境地址', max_length=100)
    proxy_host = models.CharField(verbose_name='代理地址', max_length=100,default="", blank=True)
    description = models.CharField(verbose_name='环境描述', max_length=100, blank=False, null=False)
