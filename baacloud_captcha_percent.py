#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-10 10:41:16
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import config
import helper
import image_helper

logger = helper.getLogger('percent', filePath='percent.log')


def main():
    successCount = 0
    for inx, imageFile in enumerate(config.MARKED_CAPTCHA_FOLDER.rglob('*.png')):
        logger.info('Process %s', imageFile)
        originText = imageFile.parent.name
        captchaText = image_helper.recognizeImage(imageFile)
        logger.info('Captcha %s', captchaText)
        if captchaText == originText:
            successCount += 1

    logger.info('Percent %s', (successCount / (inx + 1)))


if __name__ == '__main__':
    main()
