# encoding: utf-8
# Author    : Administrator
# Datetime  : 2020/7/27 12:27
# User      : Administrator
# Product   : PyCharm
# Project   : VrDataCenter
# File      : 002.py
# explain   : 文件说明

# 内置函数
# bif == bulit--in--function
dir(__builtins__)

print('------------------我爱鱼C工作室------------------')
temp = input("不妨猜一下小甲鱼现在心里想的是哪个数字：")
guess = int(temp)
if guess == 8:
    print("我草，你是小甲鱼心里的蛔虫吗？！")
    print("哼，猜中了也没有奖励！")
else:
    print("猜错拉，小甲鱼现在心里想的是8！")
print("游戏结束，不玩啦^_^")
"""这是注释"""
