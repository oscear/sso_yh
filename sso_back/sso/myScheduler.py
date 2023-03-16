import os
import time

from apscheduler.schedulers.background import BackgroundScheduler
import json
import logging
from httplib2 import Response
from conf.rdini import read_ini
from sso.searchFileTest import write_to_db

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='scheduler_log.txt',
                    filemode='a')


def makeCacheindex():
    '''生成文件索引，提高搜索效率'''
    print("执行成功了")
    # ip = read_ini("ResPath", "ip")
    # v = 'v8.6'
    # s = 'Chart'
    # not_found_path = []
    # testPath199 = v + "_test"  # 199 服务器的路径要加个_test  例子v8.6_test
    # halfPath = ip + testPath199 + "/assetExecute/testcases/" + s + "/res/"
    # if os.path.exists(halfPath):
    #     write_to_db(v, s, halfPath)
    # else:
    #     not_found_path.append(halfPath)


def add_task():
    _scheduler.add_job(makeCacheindex, trigger="cron", day_of_week='mon-sun', hour=18, minute=10, end_date='2030-05-30')


def remove_task(task):
    _scheduler.remove_job(task)

# replace_existing表示如果有重名的任务，直接覆盖
_scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
_scheduler.add_job(makeCacheindex, trigger="cron", day_of_week='mon-sun', hour=18, minute=18, end_date='2030-05-30',replace_existing=True)
_scheduler._logger = logging
_scheduler.start()
while True:
    time.sleep(200000)

# scheduler.remove_job('my_job_id') # 删除任务
# scheduler.pause_job('my_job_id') # 暂定任务
# scheduler.resume_job('my_job_id') # 恢复任务
