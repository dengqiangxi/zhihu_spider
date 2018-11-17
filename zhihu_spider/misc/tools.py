import hashlib
import logging
import re
import sys


def config_logger():
    logging.basicConfig(format='%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s',
                        datefmt='%a %d %b %Y %H:%M:%S', filemode='w')


def init_logger(logger_name: str, logger_path: str, debug=False):
    """
    初始化logger
    :param logger_name: logger_name
    :param logger_path: logger文件路径
    :param debug: 是否debug模式
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logger_path)
    fh.setLevel(logging.DEBUG)
    sh = logging.StreamHandler(sys.stdout) if debug else logging.NullHandler()
    sh.setLevel(logging.NOTSET)
    fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger


def format_avatar(avatar_url: str):
    if avatar_url is None:
        return ''
    return avatar_url.replace('_s.jpg', 'jpg').replace('_xl.jpg', '.jpg')


def hump2underline(hunp_str):
    '''
    驼峰形式字符串转成下划线形式
    :param hunp_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    '''
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', hunp_str).lower()
    return sub


def spelling_insert_sql(dict_keys, table_name: str):
    """
    拼接插入sql
    """
    return "insert ignore into %s (%s) values (%s)" % (table_name,
                                                       ",".join(dict_keys),
                                                       "%(" + ")s,%(".join(dict_keys) + ")s"
                                                       )


def get_ua_list():
    """
    获取ua列表
    """
    with open('zhihu_spider/misc/ua_list.txt', 'r') as f:
        return [x.replace('\n', '') for x in f.readlines()]
