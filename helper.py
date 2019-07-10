#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-03 11:24:36
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import logging
from urllib import parse as urlparse
import sys
import requests


# CLOUD_GITHUB = 'https://raw.githubusercontent.com/baacloud/baacloud.github.io/master/index.html'
API_URL = 'http://api.cn3.me/url.php?id=3'
CAPTCHA_PATH = 'other/captcha.php'
INDEX_PATH = 'modules/index.php'
LOGIN_PATH = 'modules/_login.php'
CHECKIN_PATH = 'modules/_checkin.php'

_SERVER = None

URL_CONFIG = {
    'index': INDEX_PATH,
    'login': LOGIN_PATH,
    'checkin': CHECKIN_PATH,
    'captcha': CAPTCHA_PATH
}


def getLatestServerUrl():
    global _SERVER
    if not _SERVER:
        codeRes = requests.get(API_URL)
        parseRes = urlparse.urlparse(codeRes.url)
        _SERVER = '{scheme}://{netloc}'.format(scheme=parseRes.scheme,
                                               netloc=parseRes.netloc)
    return _SERVER


def getBaacloudUrl(name):
    return urlparse.urljoin(getLatestServerUrl(), URL_CONFIG[name])


def getLogger(name, level=logging.INFO,
              stream=None, filePath=None,
              fmtStr=None, dateStr=None):
    if fmtStr is None:
        fmtStr = "<%(asctime)s> [%(name)s] [%(levelname)s] %(message)s"
    if dateStr is None:
        dateStr = '%Y-%m-%d %H:%M:%S'

    log = logging.getLogger(name)
    log.setLevel(level)

    logFmt = logging.Formatter(fmtStr,
                               datefmt=dateStr)

    if stream is None:
        stream = sys.__stdout__

    handler1 = logging.StreamHandler(stream)
    handler1.setFormatter(logFmt)
    log.addHandler(handler1)

    if filePath:
        handler2 = logging.FileHandler(filePath, 'wt')
        handler2.setFormatter(logFmt)
        log.addHandler(handler2)

    return log


if __name__ == '__main__':
    print(getLatestServerUrl())
