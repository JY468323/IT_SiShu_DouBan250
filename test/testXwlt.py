#-*- codeing = utf-8 -*-
#@Time:2022/2/27 16:38
#@Author:张佳源
#@File:testXwlt.py
#@Sofeware:PyCharm


import xlwt

workbook = xlwt.Workbook(encoding="utf-8")  #创建workbook
worksheet = workbook.add_sheet('sheet1')    #创建工作表
for i in range(1,10):
    for j in range (1,i+1):
        worksheet.write(i-1, j-1, "%d*%d=%d"%(i,j,i*j))     #写入数据，第一行参数“行”，第二个参数“列”，第三个参数内容
workbook.save('student.xls')