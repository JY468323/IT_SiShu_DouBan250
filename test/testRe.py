#-*- codeing = utf-8 -*-
#@Time:2022/2/26 21:40
#@Author:张佳源
#@File:testRe.py
#@Sofeware:PyCharm


#正则表达式：字符串模式(判断字符串是否符合一定的标准)

import re

#创建模式对象

# pat = re.compile("AA")  #此处的AA，是正则表达式，用来去验证其他的字符串
# #m = pat.search("CBA")   #search字符串被校验的内容
# m = pat.search("AABCAADDCCAAA")  #search方法，进行比对查找


#没有模式对象

# m = re.search("asd","Aasd")  #前面的字符串是规则(模板)，后面的字符串是被校验的对象

#m = re.findall("a","ASDFGHJa")  #前面的字符串是规则(模板)，后面的字符串是被校验的对象
#m = re.findall("[A-Z]","ASAsafFGHJa")
# m = re.findall("[A-Z]+","ASAsafFGHJa")
# print(m)

#sub

print(re.sub("a","A","abcdcasd")) #找到a用A替换，在第三个字符串中查找

#建议在正则表达式中，被比较的字符串前面加上r，不用担心转义字符的问题

a = r"\absda-\'"
print(a)

