# encoding: utf-8
# Author    : wangtong
# Datetime  : 2020/7/21 16:50
# User      : wangtong
# Product   : PyCharm
# Project   : VrEtl
# File      : LoadIptvSanXiDataToDB.py
# explain   : 陕西iptv数据入库到 oracle



import sys
sys.path.append(r'E:\天翼阅读\svn\1.代码类\1.VR业务\VrDataCenter\VrPythonUtailScript')
import VrPythonUtailScript_onwin as orc

## 定义数据文件路径，目标表字段
infilepath= r'C:\Users\Administrator\Desktop\11'
iptv_cols = ["date_id", "unique_user_id", "account", "content_code", "contentname", "click_time", "starttime",
             "endtime", "duration", "duration_seconds", "traffic_mb", "usertype", "provice", "proviceid"]

## 获取上传时间最近的数据文件
filename = orc.get_new_report(infilepath)
print(filename)
## 执行导入
orc.loadfileToOracle(filename, iptv_cols, 10, '610000', '陕西', '')

