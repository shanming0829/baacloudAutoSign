import collections
import config
import image_helper


def orderLabel():
    counts = collections.defaultdict(int)
    for imageFolder in config.SOURCE_CAPTCHA_FOLDER.glob('*'):
        if imageFolder.is_dir():
            captchaText = imageFolder.name
            for filename in imageFolder.glob('*.png'):
                try:
                    filename.rename(
                        imageFolder / '{}.png'.format(str(counts[captchaText] + 1).zfill(6)))
                except FileExistsError:
                    pass
                counts[captchaText] += 1


def moveFileFromFolder():
    for inx, imageFile in enumerate(config.SOURCE_CAPTCHA_FOLDER.rglob('*.png')):
        print('[INFO] Process %s' % imageFile)
        imageFile.rename(config.SOURCE_CAPTCHA_FOLDER /
                         '{}.png'.format(str(inx + 1).zfill(6)))

    for folder in config.SOURCE_CAPTCHA_FOLDER.rglob('*'):
        if folder.is_dir():
            folder.rmdir()


def main():
    # re-order exist label folder
    # orderLabel()

    counts = collections.defaultdict(int)

    # Grab some random CAPTCHA images to test against.
    # loop over the image paths
    for imageFile in config.SOURCE_CAPTCHA_FOLDER.glob('*.png'):
        print('[INFO] Process %s' % imageFile)
        # Print the captcha's text
        captchaText = image_helper.recognizeImage(str(imageFile))
        # oldText = imageFile.name.split('.')[0]
        if captchaText:
            labelDir = config.SOURCE_CAPTCHA_FOLDER / captchaText
            if labelDir.exists():
                counts[captchaText] = len(list(labelDir.glob('*.png')))
            else:
                labelDir.mkdir(exist_ok=True)

            newName = '{}.png'.format(
                str(counts[captchaText] + 1).zfill(6))
            dstFile = labelDir / newName
            imageFile.rename(dstFile)
            counts[captchaText] += 1
        else:
            imageFile.unlink()


if __name__ == '__main__':
    main()
