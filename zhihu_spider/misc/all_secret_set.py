import pymysql

mysql_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'toor',
    'db': 'zhihu',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}
cookies = {}

def get_zhihu_cookie():
    if cookies:
        print("----")
        return cookies
    f = open("cookie", "rb")
    cookie = f.read().decode("utf-8")
    f.close()
    for i in cookie.split(";"):
        line = i.replace('"', '').split("=", 1)
        cookies[line[0]] = line[1]
    return cookies