"""sso_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL_conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import routers

from sso import views
router = routers.DefaultRouter()
router.register(r'api/v1/host', views.HostViewset, basename="host")
router.register(r'api/v1/module', views.ModuleViewset, basename="module")
from django.views.static import serve
# 导入静态文件模块
from django.conf import settings
# 导入配置文件里的文件上传配置

urlpatterns = [
    path('admin/', admin.site.urls),
    url('api/v1/login/', views.LoginViewSet.as_view()),
    url('api/v1/loginsso/', views.TokenVerify.as_view()),
    re_path('api/v1/register/(?P<pk>\d+)/', views.RegisterUser.as_view(), name="edit_user"),
    url('api/v1/register/', views.RegisterUser.as_view(), name="add_user"),
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path('static/(?P<path>.*)', serve, {'document_root':settings.STATIC_ROOT}),
    url('api/v1/report/', views.JunitReport.as_view(), name="Junit_Report"),
    url('api/v1/checkLocalSVN/', views.checkLocalSVN.as_view(), name="checkLocalSVN"),
    url('api/v1/SvnCommit/', views.SvnCommit.as_view(), name="checkLocalSVN"),
    url('api/v1/AvatarUpload/', views.AvatarUpload.as_view(), name="AvatarUpload"),
]
urlpatterns += router.urls
