#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-09 13:00:45
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import pathlib

BASEDIR = pathlib.Path(__file__).parent

MODEL_DIR = BASEDIR / 'models'
IMAGE_DIR = BASEDIR / 'images'

if not MODEL_DIR.exists():
    MODEL_DIR.mkdir()

if not IMAGE_DIR.exists():
    IMAGE_DIR.mkdir()

MODEL_FILENAME = MODEL_DIR / "baacloud_captcha_model.hdf5"
MODEL_LABELS_FILENAME = MODEL_DIR / "baacloud_model_labels.dat"
SOURCE_CAPTCHA_FOLDER = IMAGE_DIR / "baacloud_source_captcha_images"
MARKED_CAPTCHA_FOLDER = IMAGE_DIR / "baacloud_marked_captcha_images"
HTML_MARKED_CAPTCHA_FOLDER = IMAGE_DIR / "baacloud_html_marked_captcha_images"
LETTER_IMAGES_FOLDER = IMAGE_DIR / "baacloud_extracted_letter_images"
