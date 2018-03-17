#!/usr/bin/env python
# -*- coding=utf8 -*-
# Created by dengqiangxi at 2018/3/17
print('请输入你要分割的 cookie,回车开始分割')
print('\n\n\n\n')
cookie = input()
for i in cookie.split(";"):
    print('"'+'":"'.join(i.replace('"','').split("=", 1))+'",')