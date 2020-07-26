
#!/usr/bin/env bash
# Author    : wangtong
# Datetime  : 2020/7/21 16:50
# User      : wangtong
# Product   : PyCharm
# Project   : VrEtl
# File      : VrPythonUtailScript.py
# explain   : 常用的功能封装


## 从path1复制新增的文件到path2，并删除path1存在的文件；
## 参数1：源地址 参数1：目标地址
function F_MoveFileToOthPath() {

datestr=`date`
tmppath=$1  #'/e/ftptest/tmpfile/'
realpath=$2 #'/e/ftptest/'
cd $realpath
for i in `ls ${tmppath}`
do
  if [ -e "$i" ]; then
    echo ${datestr}" File $i exists >>> drop file $i";
    rm ${tmppath}${i}
  else
    echo ${datestr}" File $i not found >>> move $i to $realpath"; cp ${tmppath}${i} ${realpath}${i}
  fi
done

}

## 从FTP下载文件内容
## 参数1：ip 参数2：account 参数3：password 参数2：filename 参数5：下载地址
function F_DownFtpfiles() {
echo `date`' >>> '" BEGIN"
ftp -n<<!
open $1
user $2 $3
binary
prompt
lcd $5
mget $4*
close
bye
!
for i in  `ls $5`
do
  echo `date`' >>> '$i " download success;"
done
echo `date`' >>> '" END"
}

