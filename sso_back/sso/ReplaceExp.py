# 导入模块
import os
import shutil

from conf.rdini import read_ini
from rest_framework.response import Response


def FileToLocal(version, resPath, isDis):
    path = read_ini("SvnLocal", version)
    filename = resPath.split("testcases")[-1]
    localRef = path + filename.replace("/res/", isDis)
    try:
        shutil.copyfile(resPath, localRef)
        return Response("replaceExp Successfully", status=200)
    except Exception as e:
        return Response({"error": repr(e)}, status=400)
