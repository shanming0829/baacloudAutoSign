import collections
import cv2

import config
import image_helper


def main():
    counts = collections.defaultdict(int)

    # loop over the image paths
    for labelDir in config.MARKED_CAPTCHA_FOLDER.glob('*'):
        captchaText = labelDir.name
        for captchaImage in labelDir.glob('*.png'):
            print("[INFO] processing image {}".format(captchaImage))
            letterImages = image_helper.getLetterImages(
                str(captchaImage), regionCount=4)

            # Not extract the numbers region count
            if not letterImages:
                continue

            # Save out each letter as a single image
            for letterImage, letterText in zip(letterImages, captchaText):

                # Get the folder to save the image in
                savePath = config.LETTER_IMAGES_FOLDER / letterText

                if not savePath.exists():
                    savePath.mkdir(parents=True, exist_ok=True)

                # write the letter image to a file
                imageName = "{}.png".format(str(counts[letterText]).zfill(6))
                cv2.imwrite(str(savePath / imageName), letterImage)

                # increment the count for the current key
                counts[letterText] += 1


if __name__ == '__main__':
    main()
