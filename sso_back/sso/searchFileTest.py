import os
from pathlib import Path


def locate_file(base_dir, keywords='**/*.*'):
    """
    迭代目录下所有文件
    """
    p = Path(base_dir)
    return p.glob(keywords)


def write_to_db(version, testsuite, halfPath):
    """
    写入索引文件
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_ROOT = os.path.join(BASE_DIR, 'db')
    filename = testsuite + version + ".db"
    dbfile = os.path.join(DB_ROOT, filename)

    # w 指覆盖文件
    with open(dbfile, 'w', encoding='utf-8') as f:
        for r in locate_file(halfPath):
            m = str(r).replace('\\', '/')
            f.write(f"{m}\n")



