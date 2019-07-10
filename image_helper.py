#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-07-09 13:08:17
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import pickle
import pathlib
import imutils
import cv2
from keras.models import load_model
import numpy as np

import config

LABEL_MODEL = None
MODEL = None


def resizeToFit(image, width, height):
    """
    A helper function to resize an image to fit within a given size
    :param image: image to resize
    :param width: desired width in pixels
    :param height: desired height in pixels
    :return: the resized image
    """

    # grab the dimensions of the image, then initialize
    # the padding values
    (h, w) = image.shape[:2]

    # if the width is greater than the height then resize along
    # the width
    if w > h:
        image = imutils.resize(image, width=width)

    # otherwise, the height is greater than the width so resize
    # along the height
    else:
        image = imutils.resize(image, height=height)

    # determine the padding values for the width and height to
    # obtain the target dimensions
    padW = int((width - image.shape[1]) / 2.0)
    padH = int((height - image.shape[0]) / 2.0)

    # pad the image then apply one more resizing to handle any
    # rounding issues
    image = cv2.copyMakeBorder(image, padH, padH, padW, padW,
                               cv2.BORDER_REPLICATE)
    image = cv2.resize(image, (width, height))

    # return the pre-processed image
    return image


def getLetterImages(imageFile, regionCount=4):
    imageFile = pathlib.Path(imageFile)
    # Load the image and convert it to grayscale
    image = cv2.imread(str(imageFile))
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    except cv2.error:
        print('[INFO] Image Broken: %s' % imageFile)
        return None

    # Add some extra padding around the image
    gray = cv2.copyMakeBorder(gray, 20, 20, 20, 20, cv2.BORDER_REPLICATE)

    # threshold the image (convert it to pure black and white)
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # find the contours (continuous blobs of pixels) the image
    contours = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Hack for compatibility with different OpenCV versions
    # Issue: https://stackoverflow.com/questions/48291581/how-to-use-cv2-findcontours-in-different-opencv-versions/48292371
    contours = contours[-2:][0]

    letterImageRegions = []

    # Now we can loop through each of the four contours and extract the letter
    # inside of each one
    for contour in contours:
        # Get the rectangle that contains the contour
        (x, y, w, h) = cv2.boundingRect(contour)

        # Compare the width and height of the contour to detect letters that
        # are conjoined into one chunk
        if w / h > 1.25:
            # This contour is too wide to be a single letter!
            # Split it in half into two letter regions!
            halfWidth = int(w / 2)
            letterImageRegions.append((x, y, halfWidth, h))
            letterImageRegions.append((x + halfWidth, y, halfWidth, h))
        else:
            # This is a normal letter by itself
            letterImageRegions.append((x, y, w, h))

    # Sort the detected letter images based on the x coordinate to make sure
    # we are processing them from left-to-right so we match the right image
    # with the right letter
    letterImageRegions = sorted(letterImageRegions, key=lambda x: x[0])

    letterImages = []
    # loop over the lektters
    for letterBoundingBox in letterImageRegions:
        # Grab the coordinates of the letter in the image
        x, y, w, h = letterBoundingBox

        # Extract the letter from the original image with a 2-pixel margin around the edge
        letterImage = gray[y - 2:y + h + 2, x - 2:x + w + 2]

        # Re-size the letter image to 20x20 pixels to match training data
        try:
            letterImage = resizeToFit(letterImage, 20, 20)
        except (cv2.error, ZeroDivisionError):
            pass
        else:
            letterImages.append(letterImage)

    # If we found more or less than 4 letters in the captcha, our letter extraction
    # didn't work correcly. Skip the image instead of saving bad training data!
    if regionCount and len(letterImages) != regionCount:
        return None

    return letterImages


def recognizeImage(imageFile, charCount=4, labelModel=None, model=None):
    if labelModel is None:
        global LABEL_MODEL
        if LABEL_MODEL is None:
            # Load up the model labels
            with config.MODEL_LABELS_FILENAME.open("rb") as f:
                LABEL_MODEL = pickle.load(f)
        labelModel = LABEL_MODEL
    if model is None:
        global MODEL
        if MODEL is None:
            # Load the trained neural network
            MODEL = load_model(str(config.MODEL_FILENAME))
        model = MODEL

    letterImages = getLetterImages(imageFile, charCount)
    if not letterImages:
        return None
    predictions = []
    # loop over the lektters
    for letterImage in letterImages:
        # Turn the single image into
        # a 4d list of images to make Keras happy
        letterImage = np.expand_dims(letterImage, axis=2)
        letterImage = np.expand_dims(letterImage, axis=0)

        # Ask the neural network to make a prediction
        prediction = model.predict(letterImage)

        # Convert the one-hot-encoded prediction back to a normal letter
        letter = labelModel.inverse_transform(prediction)[0]
        predictions.append(letter)

    # Print the captcha's text
    captchaText = "".join(predictions)

    return captchaText
