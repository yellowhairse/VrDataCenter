# encoding: utf-8
# Author    : wangtong
# Datetime  : 2020/7/21 16:50
# User      : wangtong
# Product   : PyCharm
# Project   : VrEtl
# File      : VrPythonUtailScript.py
# explain   : 常用的功能封装


import sys
import hashlib
import time
import cx_Oracle
import datetime
import os
import io

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

# reload(sys)
# sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("no args specified")
        filepath = r"C:\Users\Administrator\Desktop\11"
    else:
        filepath = sys.argv[1]


def get_new_report(filepath):
    '''返回目录下创建时间最新的文件的名称
     input： [filepath] [路径]
     outer： [filename]
     sample：'''
    lists = os.listdir(filepath)  # 列出目录的下所有文件和文件夹保存到lists
    lists.sort(key=lambda fn: os.path.getmtime(filepath + "/" + fn))  # 按时间排序
    filename = os.path.join(filepath, lists[-1])  # 获取最新的文件保存到file_new
    return filename


def get_userid(user_id):
    ''' 用于数据仓库内部识别的user_id【16位】与VR商用区分
     input： [user_id] [路径]
     outer： [user_id]
     sample：'''
    md5 = hashlib.md5()
    md5.update(str(user_id).encode('utf-8'))
    p = md5.hexdigest()
    as_int = int(p, 16)
    result = str(as_int)[0:16]
    return result


def loadfileToOracle(infile, cols, offset, provid='610000', provname='陕西', usertype='15'):
    '''csv 文件导入oracle
      input： [infile] [文件]
              [cols] [目标表字段]
              [offset] [时间偏移量]
              [provname] [省份]
              [provid] [省份ID]
              [usertype] [用户类型]
      outer： [MID_VR_IPTV_ACT_D]
      sample：'''

    # 定义结果集列名
    iptv_cols = cols
    offset = int(offset)
    provid = str(provid)
    usertype = str(usertype)
    insert_cols = ",".join([x for x in iptv_cols])
    count = 0  # 记录行数
    # 连接oracle
    conn = cx_Oracle.connect('jyfx', 'Vrdw^pass',
                             '10.100.10.100:1521/vrdw')  # , encoding = "UTF-8", nencoding = "UTF-8")
    cursor = conn.cursor()

    # 读取文件
    with io.open(infile, "r", encoding='gbk') as fd:
        data_lines = fd.readlines()
        for line in data_lines[1:]:  # 跳过首行
            line_datas = line.split(',')
            if len(line_datas) < 6:  # 原始数据字段判断【小于6位 跳出】
                continue
            # 对目标字段格式化处理

            content_code = line_datas[0].replace('\n', '').replace('\r\n', '')
            content_name = line_datas[1].replace('\n', '').replace('\r\n', '')
            account = line_datas[2].replace('\n', '').replace('\r\n', '')
            str_starttime = line_datas[3].replace('\n', '').replace('\r\n', '')
            starttime = datetime.datetime.strptime(str_starttime, '%Y-%m-%d %H:%M:%S')
            delta = datetime.timedelta(days=offset)  # 数据日期偏移量
            delta_starttime = starttime + delta
            str_delta_starttime = datetime.datetime.strftime(delta_starttime, '%Y-%m-%d %H:%M:%S')
            str_endtime = line_datas[4].replace('\n', '').replace('\r\n', '')
            endtime = datetime.datetime.strptime(str_endtime, '%Y-%m-%d %H:%M:%S')
            delta_endtime = endtime + delta
            str_delta_endtime = datetime.datetime.strftime(delta_endtime, '%Y-%m-%d %H:%M:%S')
            start_time = int(time.mktime(time.strptime(str_delta_starttime, '%Y-%m-%d %H:%M:%S')))
            end_time = int(time.mktime(time.strptime(str_delta_endtime, '%Y-%m-%d %H:%M:%S')))
            click_time = line_datas[5].replace('\n', '').replace('\r\n', '')
            # duration = line_datas[6].replace('\n', '').replace('\r\n', '')
            duration = ''
            unique_userid = get_userid("iptv_sx_" + account)  # 生成唯一user_id
            duration_seconds = end_time - start_time
            traffic_mb = 6 * duration_seconds  # 码率转换
            date_id = datetime.datetime.fromtimestamp(start_time).strftime("%Y%m%d")
            # 拼接insert sql
            insert_values = "(" + "\'" + date_id + "\'" + "," + "\'" + unique_userid + "\'" + "," \
                            + "\'" + account + "\'" + "," + "\'" + content_code + "\'" + "," \
                            + "\'" + content_name + "\'" + "," + "\'" + click_time + "\'" + "," \
                            + "\'" + str_delta_starttime + "\'" + "," + "\'" + str_delta_endtime + "\'" + "," \
                            + "\'" + duration + "\'" + "," + "\'" + str(duration_seconds) + "\'" + "," \
                            + "\'" + str(traffic_mb) + "\'" + "," \
                            + "\'" + usertype + "\'" + "," + "\'" + provname + "\'" + "," + "\'" + provid + "\'" + ")"
            insert_sql = "insert into MID_VR_IPTV_ACT_D_test ({}) values {}".format(insert_cols, insert_values)
            # print(insert_sql)
            try:
                cursor.execute(insert_sql)
            except Exception as e:
                print(str(e))
            count += 1
            if count % 200 == 0:
                print(time.asctime() + '>>>' + '当前导入：' + str(count) + '条数据')
                conn.commit()
        print(time.asctime() + '>>>' + '共导入：' + str(count) + '条数据')
        conn.commit()
        cursor.close()
        conn.close()

