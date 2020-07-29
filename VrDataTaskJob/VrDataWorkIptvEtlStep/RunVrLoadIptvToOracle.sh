#!/usr/bin/env bash
# Author    : wangtong
# Datetime  : 2020/7/21 16:50
# User      : wangtong
# Product   : PyCharm
# Project   : VrDataCenter
# File      : LoadIptvSanXiDataToDB.py
# explain   : iptv数据入库到 oracle


. /e/天翼阅读/svn/1.代码类/1.VR业务/VrDataCenter/VrBashUtailScript/VrBashUtailScript.sh

month=`date +%Y%m`
Scriptpath='/e/天翼阅读/svn/1.代码类/1.VR业务/VrDataCenter/VrDataTaskJob/VrDataWorkIptvEtlStep/'
# 参数1：源ip 参数2：useid 参数3：passwd 参数4：文件名【月】参数5：目标地址
# 从ftp下载文件到临时目录
F_DownFtpfiles '10.0.35.121' 'iptv_sx' 'FetcjBMKQmyO' "iptv_sx" '/data01/ExternalData/iptv/prov_sanxi_tmp/'

# 参数1：源地址 参数2：目标地址
# 新增文件放入导入数据指定路径
F_MoveFileToOthPath '/data01/ExternalData/iptv/prov_sanxi_tmp/' '/data01/ExternalData/iptv/prov_sanxi/'

# 执行入库脚本
python ${Scriptpath}VrLoadIptvToOracle.py

# 任务失败则报警
if [ $? -eq 1 ];then
    F_ReturnDingtalkSMS 'IPTV【陕西】数据抽取失败'
fi
