#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-05 10:31:06
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import collections
import queue
import threading

import cv2

import config


def showImage(imageQueue):
    cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
    while 1:
        imagePath = imageQueue.get(block=True)
        im = cv2.imread(imagePath)
        cv2.imshow("image", im)
        cv2.waitKey(1 * 1000)


def main():
    counts = collections.defaultdict(int)
    imageQueue = queue.Queue()
    imageThread = threading.Thread(target=showImage, args=(imageQueue,))
    imageThread.start()
    for filename in config.SOURCE_CAPTCHA_FOLDER.rglob('*.png'):
        imageQueue.put(str(filename))
        label = input('Image[%s] str:' % filename)

        if not label:
            label = filename.parent.name

        if label:
            labelDir = config.MARKED_CAPTCHA_FOLDER / label
            if labelDir.exists():
                counts[label] = len(list(labelDir.glob('*.png')))
            else:
                labelDir.mkdir(exist_ok=True)

            newName = '{}.png'.format(str(counts[label] + 1).zfill(6))
            filename.rename(labelDir / newName)
            counts[label] += 1


if __name__ == '__main__':
    main()
