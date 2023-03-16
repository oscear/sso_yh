import os
from pathlib import Path

import xlrd
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, FileResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render
# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from conf.rdini import read_ini
from sso.GitSvn import syncGetAllFileStatus, svnUpdateSync, svnCommitSync, svnAddSync
from sso.ParseXMLFile import parseXmlFile
from sso.ReplaceExp import FileToLocal
from sso.To_xml import ExcelToXml, OpenExcel
from sso.models import Module, Host
from sso.searchFileTest import write_to_db
from sso.serializers import ModuleSerializer, HostSerializer, UserSerializer


CustomUser = get_user_model()


class RegisterUser(APIView):
    permission_classes = (AllowAny,)  # AllowAny 允许所有用户

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        # userAlias = request.data.get("userAlias")
        # userRoles = request.data.get("userRoles")
        # userGroups = request.data.get("userGroups")
        # param = request.data.get("param")
        user = CustomUser.objects.create_user(username=username, password=password, email=email)
        user.save()
        context = {
            "code": status.HTTP_200_OK,
            "msg": "用户注册成功"
        }
        return JsonResponse(context, safe=False)

    def put(self, request, pk):
        username = request.data.get("username")
        # password = request.data.get("password")
        email = request.data.get("email")
        userAlias = request.data.get("userAlias")
        userRoles = request.data.get("userRoles")
        userGroups = request.data.get("userGroups")
        param = request.data.get("param")
        # 修改信息
        user = CustomUser.objects.filter(id=pk).update(username=username, email=email,
                                                       userAlias=userAlias,
                                                       userRoles=userRoles, userGroups=userGroups, param=param)
        # user.save()
        context = {
            "code": status.HTTP_200_OK,
            "msg": "修改信息成功"
        }
        user = CustomUser.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return JsonResponse([serializer.data], safe=False)
        # return JsonResponse(context)

    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return JsonResponse([serializer.data], safe=False)


class LoginViewSet(APIView):
    '''登录获取token方法'''
    permission_classes = (AllowAny,)  # AllowAny 允许所有用户

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        # django.contrib.auth.models.User
        user = auth.authenticate(username=username, password=password)
        if not user:
            return JsonResponse(data={"code": 401,
                                      "msg": "用户名或密码不对!"}, status=401)
        # 删除原有的Token
        old_token = Token.objects.filter(user=user)
        old_token.delete()
        # 创建新的Token
        token = Token.objects.create(user=user)
        return JsonResponse({"code": 200,
                             "message": "success!",
                             "data": token.key,
                             "uuid": user.id,
                             "username": user.username
                             }, status=200)


class Password(APIView):
    authentication_classes = (TokenAuthentication)  # 使用基础的和token的验证方式
    permission_classes = (IsAuthenticated,)  # 只允许所有通过鉴权的人访问

    def post(self, request):
        """
        修改密码
        """
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')
        if new_password1 and new_password1 == new_password2:
            request.user.set_password(new_password1)
            request.user.save()
            context = {
                "code": status.HTTP_200_OK,
                "msg": "修改密码成功"
            }
        else:
            context = {
                "status": status.HTTP_403_FORBIDDEN,
                "msg": "两次密码不一样或没密码"
            }
        return JsonResponse(context)


class Logout(APIView):
    authentication_classes = (TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        登出
        """
        # auth.logout(request)
        Token.objects.filter(user=request.user).delete()
        context = {
            "status": status.HTTP_200_OK,
            "msg": "退出成功"
        }
        return JsonResponse(context)


class TokenVerify(APIView):
    permission_classes = (AllowAny,)  # AllowAny 允许所有用户

    def post(self, request):
        '''登录获取token方法'''
        token = request.data.get("token")
        user_id = Token.objects.get(key=token).user_id
        user = CustomUser.objects.get(id=user_id)
        if user.param != "":
            param = eval(user.param)
        else:
            param = {"key": "value"}
        if user_id:
            return JsonResponse(
                {"result": "success",
                 "userId": user.username,
                 "userAlias": user.userAlias,
                 "userEmail": user.email,
                 "userRoles": user.userRoles,
                 "userGroups": user.userGroups,
                 "param": param
                 })
        else:
            return JsonResponse(data={"code": 401,
                                      "result": "error",
                                      "msg": "用户名或密码不对!"}, status=401)


class ModuleViewset(ModelViewSet):
    ''' module的crud视图 '''
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    authentication_classes = (TokenAuthentication,)  # token认证
    permission_classes = (IsAuthenticated,)  # IsAuthenticated 仅通过认证的用户


class HostViewset(ModelViewSet):
    ''' module的crud视图 '''
    serializer_class = HostSerializer
    queryset = Host.objects.all()
    authentication_classes = (TokenAuthentication,)  # token认证
    permission_classes = (IsAuthenticated,)  # IsAuthenticated 仅通过认证的用户


class JunitReport(APIView):
    """
     获取junit的failure以及 替换预期
    """
    authentication_classes = (TokenAuthentication,)  # token认证
    permission_classes = (IsAuthenticated,)  # IsAuthenticated 仅通过认证的用户

    def get(self, request):
        version = request.query_params.get("version")
        testsuite = request.query_params.get("testsuite")
        return Response(parseXmlFile(version, testsuite))

    # 替换预期
    def post(self, request):
        version = request.data.get("version")
        realPath = request.data.get("realPath")
        isDis = request.data.get("isDis")   # 判断将res图片替换到本地svn的exp 或 exp_dis
        return FileToLocal(version, realPath, isDis)




# 本地svn状态
class checkLocalSVN(APIView):

    """
    更新本地仓库
    """
    authentication_classes = (TokenAuthentication,)  # token认证
    permission_classes = (IsAuthenticated,)  # IsAuthenticated 仅通过认证的用户
    def post(self, request):
        version = request.data.get("version")
        testsuite = request.data.get("testsuite")
        modulepath = read_ini("SvnLocal", version) + testsuite
        # 更新本地仓库
        try:
            return Response(svnUpdateSync(modulepath))
        except Exception as e:
            return Response(e)

    # 查询本地文件状态
    def get(self, request):
        version = request.query_params.get("version")
        testsuite = request.query_params.get("testsuite")
        modulepath = read_ini("SvnLocal", version) + testsuite
        sthWillToSvn = syncGetAllFileStatus(modulepath)
        return Response(sthWillToSvn)


class SvnCommit(APIView):
    '''
    提交本地仓库到Svn
    '''
    authentication_classes = (TokenAuthentication,)  # token认证
    permission_classes = (IsAuthenticated,)  # IsAuthenticated 仅通过认证的用户

    def post(self, request):
        version = request.data.get("version")
        testsuite = request.data.get("testsuite")
        comment = request.data.get("comment")
        modulepath = read_ini("SvnLocal", version) + testsuite
        try:
            svnAddSync(modulepath)
            res = svnCommitSync(modulepath, comment=comment)
        except Exception as e:
            res = repr(e)
        return Response(res)


class AvatarUpload(APIView):
    # authentication_classes = (TokenAuthentication,)  # token认证
    # permission_classes = (IsAuthenticated,)  # IsAuthenticated 仅通过认证的用户

    def post(self, request):
        '''
        :param request:
        :return:  a list of sheet name
        '''
        files = request.FILES.get('file')
        book = xlrd.open_workbook(filename=None, file_contents=files.read())
        sheetnames = book.sheet_names()
        filename = files.name
        ExcelToXml(book, filename, sheetnames).to_xml()
        return Response(sheetnames)

    def get(self, request):
        '''
        :param request:
        :return: a file
        '''
        BASE_DIR = Path(__file__).resolve().parent.parent
        xml_ROOT = os.path.join(BASE_DIR, 'testlink')
        sheetname = request.query_params.get("sheetname")
        demo = "demo.xlsx"
        if sheetname:
            sheetname = sheetname + ".xml"
            filepath = os.path.join(xml_ROOT, sheetname)
        else:
            filepath = os.path.join(xml_ROOT, demo)
        filename = sheetname if sheetname else demo
        if os.path.exists(filepath):
            response = FileResponse(open(filepath, 'rb'))  # 生成文件对象application/msword  application/octet-stream
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename ="%s"' % (
                filename.encode('utf-8').decode('ISO-8859-1'))
            return response
        else:
            return Response({"notFound": sheetname}, status=400)







