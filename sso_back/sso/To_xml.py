# -*- coding:gbk -*-
from pathlib import Path

import xlrd
import os
import collections
import xml.dom.minidom

BASE_DIR = Path(__file__).resolve().parent.parent
xml_ROOT = os.path.join(BASE_DIR, 'testlink')

class OpenExcel:
    def __init__(self, book, filename, sheetname):
        self.book = book
        self.filename = filename
        self.sheetname= sheetname
        # self.excel_data = xlrd.open_workbook(self.book)
        self.sheet_data = self.book.sheet_by_name(self.sheetname)
        self.sheets_name = []
        self.sheet_nrows = ''
        self.sheet_ncols = ''
        self.row_value = []
        self.tag_list = []
        self.all_list = []

    def get_nrows(self):
        self.sheet_nrows = self.sheet_data.nrows
        return self.sheet_nrows

    def get_tag_list(self):
        # 第一行当做字典key值
        self.tag_list = self.sheet_data.row_values(0)
        return self.tag_list

    def get_row_value(self, row_num):
        self.row_value = self.sheet_data.row_values(row_num)
        return self.row_value

    def data_list(self):
        # 从第二行开始循环行并且写入list，每一行为一个dic
        for row_num in range(1, self.get_nrows()):
            row_dic = collections.OrderedDict(zip(self.get_tag_list(), self.get_row_value(row_num)))
            self.all_list += [row_dic]
        return self.all_list


class DicToXml:

    def __init__(self, data, xmlFileName):
        self.xmlFileName = xmlFileName
        self.data_list = data # open_excel解析出来的list
        self.row = ''
        self.tag = list(data[0].keys())
        self.step_num = 0
        self.dom = xml.dom.minidom.getDOMImplementation().createDocument(None, 'testcases', None)

    def get_importance(self, temporary_row ):
        # 解决没有写importance的情况
        if self.data_list[temporary_row]['Importance'] == '':
            return '3'
        else:
            return str(int(self.data_list[temporary_row]['Importance']))

    def get_name(self,temporary_row):
        if 'Name' in self.tag:
            return self.data_list[temporary_row]['Name']
        else:
            return self.data_list[temporary_row][self.tag[1]]

    def get_status(self,temporary_row):
        if 'Status' in self.tag:
            return  str(self.data_list[temporary_row]['Status'])
        else:
            return  str(self.data_list[temporary_row][2])

    def get_summary(self, temporary_row):
        if 'Summary' in self.tag:
            return self.data_list[temporary_row]['Summary']
        else:
            return self.data_list[temporary_row][self.tag[4]]

    def get_preconditions(self, temporary_row):
        if 'Preconditons' in self.tag:
            return self.data_list[temporary_row]['Preconditons']
        else:
            return self.data_list[temporary_row][self.tag[5]]

    def get_actions(self, temporary_row):
        if 'Actions' in self.tag:
            return self.data_list[temporary_row]['Actions']
        else:
            return self.data_list[temporary_row][self.tag[6]]

    def get_expectedresults(self, temporary_row):
        if 'Expected Results' in self.tag:
            return self.data_list[temporary_row]['Expected Results']
        else:
            return self.data_list[temporary_row][self.tag[7]]

    def get_node_execution_type(self,temporary_row):
        execution_type = self.dom.createElement('execution_type')
        if len(str(self.data_list[temporary_row]['AutoCaseName']).strip())==0:
            execution_type.appendChild(self.dom.createCDATASection('1'))
        else:
            execution_type.appendChild(self.dom.createCDATASection('2'))
        return execution_type

    def add_cdata(self, value=''):
        return self.dom.createCDATASection(value)

    def add_node(self):
        root = self.dom.documentElement
        for self.row in range(0, len(self.data_list)):
            # print(self.data_list[self.row])
            self.step_num += 1
            if self.get_name(self.row) != '':
                # 初始化步骤数，每次有Name开始算一个新用例
                self.step_num = 1

                testcase = self.dom.createElement('testcase')
                testcase.setAttribute('name', self.get_name(self.row))
                testcase.setAttribute('internalid', '')
                root.appendChild(testcase)

                node_order = self.dom.createElement('node_order')
                node_order.appendChild(self.add_cdata())
                testcase.appendChild(node_order)

                externalid = self.dom.createElement('externalid')
                externalid.appendChild(self.add_cdata())
                testcase.appendChild(externalid)

                version = self.dom.createElement('version')
                version.appendChild(self.add_cdata())
                testcase.appendChild(version)

                summary = self.dom.createElement('summary')
                summary.appendChild(self.add_cdata(self.get_summary(self.row)))
                testcase.appendChild(summary)

                preconditions = self.dom.createElement('preconditions')
                preconditions.appendChild(self.add_cdata(self.get_preconditions(self.row)))
                testcase.appendChild(preconditions)

                testcase.appendChild(self.get_node_execution_type(self.row))

                importance = self.dom.createElement('importance')
                importance.appendChild(self.add_cdata(self.get_importance(self.row)))
                testcase.appendChild(importance)

                status = self.dom.createElement('status')
                status.appendChild(self.add_cdata(self.get_status(self.row)))
                testcase.appendChild(status)

                steps = self.dom.createElement('steps')
                testcase.appendChild(steps)

                custom_fields = self.dom.createElement('custom_fields')
                testcase.appendChild(custom_fields)

                for i in range(8,len(self.tag)):
                    custom_field = self.dom.createElement('custom_field')
                    custom_fields.appendChild(custom_field)
                    name=self.dom.createElement('name')
                    name.appendChild(self.add_cdata(self.tag[i]))
                    value=self.dom.createElement('value')
                    value.appendChild(self.add_cdata(str((self.data_list[self.row][self.tag[i]]))))
                    custom_field.appendChild(name)
                    custom_field.appendChild(value)

                temporary_row = self.row + 1
                if temporary_row < len(self.data_list):
                    if ((self.get_name(temporary_row) != '' and self.get_actions(temporary_row) != '')
                            or (self.get_name(temporary_row) == '' and self.get_actions(temporary_row) == '')):
                        # 换行为步骤
                        actions = self.get_actions(self.row).split('\n')
                        results = self.get_expectedresults(self.row).split('\n')
                        # 判断步骤行数是否和结果行数一致，不一样则添加结果行数
                        while len(actions) > len(results):
                            results.append('')
                        for step_num in range(0, len(actions)):
                            steps.appendChild(self.add_step(step_num + 1, actions[step_num], results[step_num]))
                    elif self.get_name(temporary_row) == '' and self.get_actions(temporary_row) != '':
                        steps.appendChild(self.add_step(self.step_num,
                                                        self.get_actions(self.row),
                                                        self.get_expectedresults(self.row)
                                                        ))
                else:
                    actions = self.get_actions(self.row).split('\n')
                    results = self.get_expectedresults(self.row).split('\n')
                    while len(actions) > len(results):
                        results.append('')
                    for step_num in range(0, len(actions)):
                        steps.appendChild(self.add_step(step_num + 1, actions[step_num], results[step_num]))
            else:
                if self.get_actions(self.row) == '':
                    pass
                else:
                    steps.appendChild(self.add_step(self.step_num,
                                                    self.get_actions(self.row),
                                                    self.get_expectedresults(self.row)
                                                    ))

    def add_step(self, step_num, step_actions, step_results):
        step = self.dom.createElement('step')
        step_number = self.dom.createElement('step_number')
        step_number.appendChild(self.add_cdata(str(step_num)))
        step.appendChild(step_number)

        actions = self.dom.createElement('actions')
        actions.appendChild(self.add_cdata(step_actions))
        step.appendChild(actions)

        expectedresults = self.dom.createElement('expectedresults')
        expectedresults.appendChild(self.add_cdata(step_results))
        step.appendChild(expectedresults)

        step.appendChild(self.get_node_execution_type(self.row))

        return step

    def write_to_xml(self):
        xmlFileName = self.xmlFileName + '.xml'
        f = open(xmlFileName, "w", encoding='utf-8 ')
        self.dom.writexml(f, addindent='\t', newl='\n', encoding='UTF-8')
        f.close()


class ExcelToXml:

    def __init__(self, book, filename, sheetnames, xml_file=''): # 修改sfs  多一个book
        self.book = book
        self.filename = filename
        self.sheetname = sheetnames
        self.xml_file = xml_file
        self.DEBUG_FLAG = False

    def get_sheets_name(self):
        excel_data = xlrd.open_workbook(self.filename)
        # 读取并筛选出没有隐藏的sheet页，“_sheet_visibility”为0
        sheets = excel_data.sheet_names()
        for index in range(0, len(sheets)):
            if excel_data._sheet_visibility[index] == 0:
                self.sheetname.append(sheets[index])
        return self.sheetname

    def to_xml(self):
        # if self.xml_file == '':
        #     path = self.filename.split('.')[0]
        # else:
        #     path = self.xml_file
        #
        # if not os.path.exists(path):
        #     os.makedirs(path)

        path = xml_ROOT   # 更改目录 ，修改sfs
        print("path",path)

        try:
            if len(self.sheetname) == 0:
                self.sheetname = self.get_sheets_name()
        except Exception as err:
            print("没有找到" + self.filename)
            print(err)

        for sheet in self.sheetname:
            if self.DEBUG_FLAG:
                xmlFileName = path + '/' + sheet
                # open_excel 解析excel为list
                data = OpenExcel(self.book,self.filename, sheet).data_list()
                test = DicToXml(data, xmlFileName)
                test.add_node()
                test.write_to_xml()
                print(sheet + '转换成功')
            else:
                try:
                    xmlFileName = path + '/' + sheet   # 适配linux  将\\改为/
                    # open_excel 解析excel为list
                    data = OpenExcel(self.book, self.filename, sheet).data_list()
                    test = DicToXml(data, xmlFileName)
                    test.add_node()
                    test.write_to_xml()
                    print(sheet + '转换成功')
                except Exception as err:
                    print(sheet + '没有转换成功')
                    print(err)
                continue


if __name__ == "__main__":
    DEBUG_FLAG = False

    filename = input('输入转换excel表格路径及名称（含后缀）：\n')
    sheetnames = []
    sheetname = input('输入需要转换的sheet页（区分大小写，可以为空，输入空时结束，没有输入则转换所有sheet）:\n')
    while sheetname != '':
        sheetnames.append(sheetname)
        sheetname = input()
    xml_file = input('输入xml目标文件夹（可以为空）：\n')
    ExcelToXml(filename, sheetnames, xml_file).to_xml()
    print('\n 任务执行完成')
    input()
