import configparser
import os

path = os.path.dirname(os.path.abspath(__file__))


def read_ini(section, name):
    rf = configparser.ConfigParser()
    inipath = os.path.join(path, 'conf.ini')
    # rf.read("..\Config\conf.ini")
    rf.read(inipath, encoding="utf-8-sig")
    key = rf.get(section, name)
    return key
#
# LocalRef = read_ini("ExpPath", "v10.0")
# print(LocalRef)
