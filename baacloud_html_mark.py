#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-10 14:17:49
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import collections
import queue
import threading

import flask
from flask import request, render_template, redirect

import config
import helper

Image = collections.namedtuple('Image', ['path', 'text'])
sourceDir = config.SOURCE_CAPTCHA_FOLDER
staticUrl = '/static/'

logger = helper.getLogger('baacloud')

imageQueue = queue.Queue()


def getImages(maxNumber=10):
    return list(sourceDir.rglob('*.png'))[:maxNumber]


app = flask.Flask('Baacloud',
                  static_url_path='/static',
                  static_folder=str(config.SOURCE_CAPTCHA_FOLDER))


def saveImage():
    while 1:
        imageFile, text = imageQueue.get()
        logger.info('Process %s', imageFile)
        if imageFile.exists():
            labelDir = config.MARKED_CAPTCHA_FOLDER / text
            if labelDir.exists():
                count = len(list(labelDir.glob('*.png')))
            else:
                labelDir.mkdir(parents=True, exist_ok=True)
                count = 0

            imageFile.rename(
                labelDir / '{}.png'.format(str(count + 1).zfill(6)))


def hanldleForm(formData):
    for imagePath, text in formData.items():
        imagePath = sourceDir / imagePath.replace(staticUrl, '')
        imageQueue.put((imagePath, text))


@app.route('/mark', methods=['GET', 'POST'])
def handleImage():
    if request.method == 'GET':
        allImages = [img.relative_to(sourceDir) for img in getImages()]
        staticImages = [Image('{}{}'.format(staticUrl, img),
                              img.parent.name) for img in allImages]
        return render_template('baacloud_mark_image.html',
                               images=staticImages)
    else:
        hanldleForm(request.form)
        return redirect('/mark')


@app.route('/', methods=['GET'])
def index():
    return redirect('/mark')


def main():
    handleThread = threading.Thread(target=saveImage)
    handleThread.start()
    app.run()


if __name__ == '__main__':
    main()
