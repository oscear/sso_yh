import os
import re
import xml.etree.ElementTree as ET
import time
from pathlib import Path

from conf.rdini import read_ini

xmlname = {
    "Chart": "TEST-Chart.ChartTest.xml",
    "CustomerBug": "TEST-CustomerBug.CustomerBugTest.xml",
    "DBDataprocess": "TEST-DBDataprocess.DBDataprocessTest.xml",
    "DBPainter": "TEST-DBPainter.DBPainterTest.xml",
    "DBQuery": "TEST-DBQuery.DBQueryTest.xml",
    "DynamicCalc": "TEST-DynamicCalc.DynamicCalcTest.xml",
    "Export": "TEST-Export.ExportTest.xml",
    "Mobile": "",
    "Query": "TEST-Query.QueryTest.xml",
    "R": "",
    "VPM": "TEST-VPM.VPMTest.xml"
}


def parseXmlFile(version, testsuite):
    '''
    :param version:
    :param testsuite:
    :return:
    '''
    res = []
    rowId = 0
    # 先把xml路径拼出来
    ip = read_ini("ResPath", "ip")
    testPath199 = version + "_test"  # 199 服务器的路径要加个_test  例v8.6_test
    cur_suite = xmlname.get(testsuite)
    reportXML = ip + testPath199 + "/assetExecute/reports/" + cur_suite
    # 读xml
    tree = ET.parse(reportXML)
    root = tree.getroot()
    halfPath = ip + testPath199 + "/assetExecute/testcases/" + testsuite + "/res/"
    start1 = time.time()
    for child in root.iter(tag="testcase"):
        # 第二层节点的标签名称和属性
        if child.getchildren():
            '''有子节点的'''
            rowId += 1
            CasePath = child.get("name").split("/")
            CaseHalf = '/'.join(CasePath[:-1])
            Casename = CasePath[-1]
            ResPath = os.path.join(halfPath, CaseHalf)
            failText = child.findtext("failure")
            CasePng = list(set(re.findall(CaseHalf + '/(.*?)["|<]', failText)))  # 需要替换的预期结果
            caseChildren = []
            for i in CasePng:
                previewUrl = "//192.168.1.199/bi/branch/" + version + "/test/assetExecute/testcases/" + testsuite + "/res/" + CaseHalf + "/" + i
                previewUrl = previewUrl if version.find("trunk") else previewUrl.replace("/branch", "")
                caseChildren.append(
                    {"id": rowId, "name": i, "previewUrl": previewUrl, "realPath": os.path.join(ResPath, i)})
                rowId += 1
            # 搜索文件
            res.append({"id": rowId, 'name': child.get("name"),
                        "children": caseChildren})
    end1 = time.time()
    print("总共时间花费", end1 - start1)
    return res

# parseXmlFile("v10.0","DBDataprocess")
