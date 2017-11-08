print(u'请输入你要分割的 cookie,回车开始分割')
str = input()
print('\n\n\n\n\n\n')
arr = str.split(';')
for i in arr:
    i = '"' + i
    if not i.startswith('"'):
        i = '"' + i
    if not i.endswith('"'):
        i += '"'
    i += ','
    arrs = i.split('=', 1)
    if not arrs[0].endswith('"'):
        arrs[0] += '"'
    if not arrs[1].startswith('"'):
        arrs[1] = '"' + arrs[1]
    print(':'.join(arrs))

