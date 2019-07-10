#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-03 11:19:08
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
from concurrent.futures import ThreadPoolExecutor
import pathlib
import requests
from fake_useragent import UserAgent

import helper
import config

SERVER = helper.getLatestServerUrl()
CAPTCHA_URL = helper.getCaptchaUrl()


HEADER = {
    'content-type': 'application/x-www-form-urlencoded',
    'origin': SERVER,
    'user-agent': UserAgent().chrome
}


def saveImage(imageName):
    imagePath = config.SOURCE_CAPTCHA_FOLDER / \
        '{}.png'.format(str(imageName).zfill(6))
    res = requests.get(CAPTCHA_URL, headers=HEADER)
    with imagePath.open('wb') as f:
        f.write(res.content)
    return str(imagePath)


def downloadCaptcha(maxNumbers):
    with ThreadPoolExecutor(os.cpu_count() * 4) as pool:
        images = pool.map(saveImage, range(maxNumbers))
        return list(images)


def main():
    downloadCaptcha(10000)


if __name__ == '__main__':
    main()
