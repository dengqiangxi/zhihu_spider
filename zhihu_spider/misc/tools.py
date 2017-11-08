import hashlib


def getId(url):
    return hashlib.sha1(url.encode('utf-8')).hexdigest()