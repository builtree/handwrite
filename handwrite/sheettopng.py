import os
import sys

import cv2

ASCII = list(map(chr, range(127)))
# Seq: A-Z, a-z, 0-9
RANGES = [(65, 91), (97, 123), (48, 58)]
SPECIAL_CHARACTERS = [
    ".",
    ",",
    ";",
    ":",
    "!",
    "?",
    '"',
    "'",
    "-",
    "+",
    "=",
    "/",
    "%",
    "&",
    "(",
    ")",
    "[",
    "]",
]


class SheetToPNG:
    LETTER_NAMES = [
        item for start, end in RANGES for item in ASCII[start:end]
    ] + SPECIAL_CHARACTERS

    def __init__(self, sheet, letters_dir, cols=8, rows=10):
        self.cols = cols
        self.rows = rows

        # TODO If directory given instead of image file, read all images and wrtie the images
        # (example) 0.png, 1.png, 2.png inside every character folder in letters/

        # sheet_images = []
        # for s in os.listdir(sheet_dir):
        #     sheet_images.append(cv2.imread(sheet_dir + "/" + s))

        letters = self.detectLetters(sheet)
        self.createLetterDirectory(letters, letters_dir)

    def detectLetters(self, sheet_image):
        image = cv2.imread(sheet_image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1],])
        # filtered = cv2.filter2D(blurred, -1, kernel)

        ret, thresh = cv2.threshold(gray, 200, 255, 1)
        close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, close_kernel, iterations=2)

        contours, h = cv2.findContours(
            close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = sorted(
            filter(
                lambda cnt: len(
                    cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
                )
                == 4,
                contours,
            ),
            key=cv2.contourArea,
            reverse=True,
        )

        x, y, w, h = cv2.boundingRect(contours[0])
        space_h, space_w = 7 * h // 16, 7 * w // 16

        letters = []
        j = 0
        for i in range(self.rows * self.cols):
            x, y, w, h = cv2.boundingRect(contours[i])
            cx, cy = x + w // 2, y + h // 2

            roi = image[cy - space_h : cy + space_h, cx - space_w : cx + space_w]
            letters.append([roi, cx, cy])
            j += 1

        letters.sort(key=lambda x: x[2])
        sorted_letters = []
        for k in range(self.rows):
            sorted_letters.extend(
                sorted(letters[self.cols * k : self.cols * (k + 1)], key=lambda x: x[1])
            )

        return sorted_letters

    def createLetterDirectory(self, letters, letters_dir):
        if not os.path.exists(letters_dir):
            os.mkdir(letters_dir)

        for k, images in enumerate(letters):
            letter = os.path.join(letters_dir, str(ord(self.LETTER_NAMES[k])))
            if not os.path.exists(letter):
                os.mkdir(letter)
            cv2.imwrite(
                os.path.join(letter, str(ord(self.LETTER_NAMES[k])) + ".png"),
                images[0],
            )


def main():
    if len(sys.argv) > 1:
        a = SheetToPNG(sheet=sys.argv[1], letters_dir=sys.argv[2], cols=8, rows=10,)
    else:
        print("Usage: sheettopng [SHEET_PATH] [LETTER_DIRECTORY_PATH]")
