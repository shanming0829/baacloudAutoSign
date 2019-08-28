#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-06-20 14:47:30
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import datetime
import getpass
import json
import time
import re
import pathlib

import requests
from fake_useragent import UserAgent
from lxml import html
import helper
import image_helper

logger = helper.getLogger('Baacloud')

CURRENT_TIME = datetime.datetime.now()
BASEDIR = pathlib.Path(__file__).parent
CONFIG_FILE = BASEDIR / 'config/baacloud.json'

HEADER = {
    'content-type': 'application/x-www-form-urlencoded',
    'origin': helper.getLatestServerUrl(),
    'user-agent': UserAgent().chrome
}


def string(data):
    if isinstance(data, bytes):
        return data.decode()
    return data


def get_config():
    if not CONFIG_FILE.exists():
        config = {}
        config['username'] = input('Email:')
        config['password'] = getpass.getpass()
        CONFIG_FILE.parent.mkdir(exist_ok=True)
        with CONFIG_FILE.open('wt') as f:
            f.write(json.dumps(config))
    else:
        config = json.load(CONFIG_FILE.open())
    return config


class Baacloud(object):
    """docstring for Baacloud"""

    def __init__(self, username, password):
        super(Baacloud, self).__init__()
        self.username = username
        self.password = password
        self._session = None

    @property
    def session(self):
        if not self._session:
            session = requests.Session()
            session.headers.update(HEADER)
            # session.verify = False
            self._session = session

        return self._session

    def responseText(self, response):
        # try:
        #     resText = response.text
        # except json.JSONDecodeError:
        #     resText = response.content.decode('utf-8-sig')
        resText = response.content.decode('utf-8-sig')

        return resText

    def login(self):
        url = helper.getBaacloudUrl('login')
        logger.info('Login server[%s] with [%s]',
                    helper.getLatestServerUrl(), self.username)
        postData = {
            'email': self.username,
            'passwd': self.password,
            'remember_me': 'week'
        }

        response = self.session.post(url, data=postData)
        resText = self.responseText(response)
        logger.debug(resText)
        loginData = json.loads(resText)
        if loginData['ok'] == '1':
            logger.info('Login successful...')
            return True
        logger.info('Login falure...')
        CONFIG_FILE.unlink()
        return False

    def getLastSignTime(self):
        indexFile = 'index.html'
        url = helper.getBaacloudUrl('index')
        response = self.session.get(url)

        # resText = self.responseText(response)
        with open(indexFile, 'wb') as f:
            f.write(response.content)

        root = html.parse(indexFile)
        timeXpath = '/html/body/div/div/section[2]/div[2]/div[3]/div/div[2]/p[4]/code'
        nodes = root.xpath(timeXpath)
        timeNode = nodes[0]
        return datetime.datetime.strptime(timeNode.text, '%Y-%m-%d %H:%M:%S')

    def checkSignTime(self, lastTime):
        can_sign = lastTime + datetime.timedelta(days=1)
        if CURRENT_TIME < can_sign:
            logger.error('Not over 24h, delta time: %s',
                         (can_sign - CURRENT_TIME))
            return False
        return True

    def checkIn(self):
        logger.info('Sign the captcha image')
        captchaImg = 'captcha.png'
        captchaUrl = helper.getBaacloudUrl('captcha')
        with open(captchaImg, 'wb') as img:
            img.write(self.session.get(captchaUrl).content)

        captchaText = image_helper.recognizeImage(captchaImg)
        logger.info('Detect captcha image text: %s', captchaText)

        if captchaText:
            checkinUrl = helper.getBaacloudUrl('checkin')
            response = self.session.get(checkinUrl,
                                        params={'captcha': captchaText})

            # "<script>alert('获得了294MB流量!');self.location=document.referrer;</script>"
            match = re.search(r'alert\(\'(.*?)\'\)', response.text)
            if match.group(1) == '验证码错误!':
                logger.error('Error sign code...')
                return False
            logger.info('Sign successful with %s', match.group(1))
            return True

    def run(self):
        if self.login():
            lastSignTime = self.getLastSignTime()
            if self.checkSignTime(lastSignTime):
                while not self.checkIn():
                    time.sleep(1)


def main():
    config = get_config()
    baacloud = Baacloud(config['username'], config['password'])
    baacloud.run()


if __name__ == '__main__':
    main()
