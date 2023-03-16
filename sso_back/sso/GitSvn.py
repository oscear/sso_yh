"""
具体实现逻辑
"""
# -*- coding: utf-8 -*-
import os
import pprint
import subprocess
import time
from threading import Thread
from xmltodict import parse as xmlParse

"""
SVN状态对照表
"""


class FileState:
    Normal = 0  # 000000 正常在svn管理下的最新的文件
    RemoteLocked = 1  # 000001 云端锁定态
    LocalLocked = 2  # 000010 本地锁定态
    Locked = 3  # 000011 已锁定 state and Locked == True
    LocalMod = 4  # 000100 本地有修改需提交
    RemoteMod = 8  # 001000 远程有修改需要更新
    Conflicked = 12  # 001100 冲突 state and Conflicked == Conflicked
    UnVersioned = 16  # 010000 未提交到库
    Error = 32  # 100000 错误状态


# 命令行运行
def _doSvnCommandSync(args):
    startupinfo = subprocess.STARTUPINFO()  # 只有windows生效
    startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    p = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        startupinfo=startupinfo,
        shell=True
    )
    rst, err = p.communicate()
    try:
        rst = str(rst, 'utf-8')
    except:
        rst = str(rst, 'gbk', errors="-ignore")
    try:
        err = str(err, 'utf-8')
    except:
        err = str(err, 'gbk', errors="-ignore")
    return rst, err


# svn commit --no-unlock
def svnCommitNoUnlockSync(path, comment=""):
    rst, err = _doSvnCommandSync("svn commit " + path + " -m \"" + comment + "\"" + " --no-unlock")
    return rst, err


# svn commit
def svnCommitSync(path, comment=""):
    rst, err = _doSvnCommandSync("svn commit " + path + " -m \"" + comment + "\"")
    return rst, err


# svn status
def _svnStatusSync(path):
    rst, err = _doSvnCommandSync("svn status " + path)
    if err:
        return None, err
    data = rst
    return data, None


# svn add
def svnAddSync(path):
    data, err = _doSvnCommandSync("svn add " + path + " --no-ignore --force")
    return data, err


# svn update
def svnUpdateSync(path):
    data, err = _doSvnCommandSync("svn update " + path)
    return data, err


# svn delete
def svnDeleteSync(path):
    return _doSvnCommandSync("svn delete " + path)


# svn lock
def svnLockSync(path):
    rst, err = _doSvnCommandSync("svn lock -m '哈哈哈哈哈哈' " + path)
    return rst, err


# svn unlock
def svnUnLockSync(path):
    rst, err = _doSvnCommandSync("svn unlock " + path)
    return rst, err


# svn status -u --xml 取 path路径下所有文件的svn状态
def _svnStatusXMLSync(path):
    rst, err = _doSvnCommandSync("svn status " + path + " -u --xml")
    if err:
        return None, err
    data = rst
    data = xmlParse(data)
    return data, None


# 解析xml 可以得到锁的相关信息、提交信息、文件状态
def syncGetAllFileStatus(rootPath):
    data, info = _svnStatusXMLSync(rootPath)
    returnDict = {}
    returnList = []
    lockRole = ""
    state = FileState.Normal
    if info:
        if data is None:
            state = state | FileState.UnVersioned
        else:
            state = state | FileState.Error
        print("returnDict111", returnDict)
        return returnDict
    target = data["status"]["target"]

    if target and "entry" in target:
        iterList = []
        if not isinstance(target["entry"], list):
            iterList.append(target["entry"])
        else:
            iterList = target["entry"]
        for fileStatusItem in iterList:
            state = FileState.Normal
            filePath = fileStatusItem["@path"]
            wc_status = fileStatusItem["wc-status"]
            if "unversioned" == wc_status["@item"]:
                state = state | FileState.UnVersioned
            elif "modified" == wc_status["@item"]:
                state = state | FileState.LocalMod
            elif "repos-status" in fileStatusItem:
                repos_status = fileStatusItem["repos-status"]
                if "lock" in repos_status and "lock" not in wc_status:
                    info = repos_status["lock"]["owner"]
                    lockRole = info
                    state = state | FileState.RemoteLocked
                elif "lock" in wc_status:
                    info = wc_status["lock"]["owner"]
                    lockRole = info
                    state = state | FileState.LocalLocked
                elif "modified" == repos_status["@item"]:
                    state = state | FileState.RemoteMod
                    info = "%s is modified on remote, you need update first" % filePath
                if "modified" == wc_status["@item"]:
                    state = state | FileState.LocalMod
                    info = "%s is modified on local, you need commit first" % filePath
            returnDict[os.path.normcase(filePath)] = [state, info, lockRole]
            yy = repr(filePath)
            xx = filePath.split(u'\\')[-1]
            returnList.append({"file": filePath, "state": state, "info": info, "lockRole": lockRole})
    return returnList


def openTortoise():
    pathsStr = "".join("G:\SVNCheckOut\Txt2")
    cmd = "TortoiseProc.exe /command:commit /path %s" % pathsStr
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        shell=True
    )


# openTortoise()
# data = syncGetAllFileStatus(r"F:\aMyProbjects\SSO平台\10.0\CustomerBug")
# pprint.pprint(data)
# os.system("Pause")

# svn更新操作
# svnUpdateSync(r"F:\aMyProbjects\SSO平台\10.0\CustomerBug\exp\CustomerBugAuto")
