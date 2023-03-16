import pathlib
from pathlib import Path
import time

from conf.rdini import read_ini


def locate_file(base_dir, keywords='**/*.*'):
    """
    迭代目录下所有文件
    """
    p = Path(base_dir)
    return p.glob(keywords)

def write_to_db(version,testsuite):
    """
    写入索引文件
    """
    dirs = r"\\192.168.1.199\v10.0_test\assetExecute\testcases\DBPainter\res"
    current_path = pathlib.PurePath(__file__).parent
    dbfile = current_path.joinpath("../db/DBPainterv10.0.db")

    # result = []
    # for files in locate_file(dirs):
    #     result.append(files)
    with open(dbfile, 'w', encoding='utf-8') as f:
        for r in locate_file(dirs):
            f.write(f"{str(r)}\n")


# 遍历目录

time1 = time.clock()
write_to_db("version", "testsuite")
time2 = time.clock()
print("本次运行：", time2-time1)

