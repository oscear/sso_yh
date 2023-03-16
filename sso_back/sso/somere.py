import re

text = '''
 Result[<a href="file:\\\/home/bi/branch/v10.0/test/assetExecute/testcases/CustomerBug/res/CustomerBugAuto/bug41376 _dynamic__图表1__RT.png" target="/home/bi/branch/v10.0/test/assetExecute/testcases/CustomerBug/res/CustomerBugAuto/bug41376 _dynamic__图表1__RT.png">/CustomerBug/res/CustomerBugAuto/bug41376 _dynamic__图表1__RT.png</a>]
 Expect[<a href="file:\\\/home/bi/branch/v10.0/test/assetExecute/testcases/CustomerBug/exp/CustomerBugAuto/bug41376 _dynamic__图表1__RT.png" target="/home/bi/branch/v10.0/test/assetExecute/testcases/CustomerBug/exp/CustomerBugAuto/bug41376 _dynamic__图表1__RT.png">/CustomerBug/exp/CustomerBugAuto/bug41376 _dynamic__图表1__RT.png</a>]
 Diffs [<a href="file:\\\/home/bi/branch/v10.0/test/assetExecute/testcases/CustomerBug/diffs/CustomerBugAuto/bug41376 _dynamic__图表1__RT.png" target="/home/bi/branch/v10.0/test/assetExecute/testcases/CustomerBug/diffs/CustomerBugAuto/bug41376 _dynamic__图表1__RT.png">/CustomerBug/diffs/CustomerBugAuto/bug41376 _dynamic__图表1__RT.png</a>]<br>
	at db.DBTestCase.test(DBTestCase.java:389)
	'''

regxp = '/home/(.*?)"'

xx = re.findall(regxp,text)
print(xx.__len__())