import os

import cv2

import numpy as np

NUM = 7
ASCII = list(map(chr, range(127)))
RANGES = [(48, 58), (65, 91), (97, 123)]


class SheetToPNG:
    LETTER_NAMES = [item for start, end in RANGES for item in ASCII[start:end]]

    def __init__(self, sheet_dir, letters_dir, cols, rows=9):
        self.cols = cols
        self.rows = rows

        sheet_images = []
        for s in sorted(os.listdir(sheet_dir)):
            sheet_images.append(cv2.imread(sheet_dir + "/" + s))

        letters = self.detectLetters(sheet_images)
        self.createLetterDirectory(letters, letters_dir)

    def detectLetters(self, sheet_images):
        letters = [[] for _ in range(self.rows)]

        min_area = 4000
        max_area = 5500
        i = 0

        for image in sheet_images:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # blurred = cv2.medianBlur(gray, 3)

            # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1],])
            # filtered = cv2.filter2D(blurred, -1, kernel)

            ret, thresh = cv2.threshold(gray, 200, 255, 1)
            close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            close = cv2.morphologyEx(
                thresh, cv2.MORPH_CLOSE, close_kernel, iterations=2
            )

            contours, h = cv2.findContours(
                close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )

            for cnt in contours:
                approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
                area = cv2.contourArea(cnt)
                if len(approx) == 4 and area > min_area and area < max_area:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cx, cy = x + w // 2, y + h // 2

                    roi = image[cy - 30 : cy + 30, cx - 30 : cx + 30]
                    if i < 56:
                        letters[-2 - i // self.cols].append([roi, cx])
                    elif 105 < i < 112:
                        letters[(i - 49) // self.cols].append([roi, cx])
                    i += 1

        for images in letters:
            images.sort(key=lambda x: x[1])

        return letters

    def createLetterDirectory(self, letters, letters_dir):
        if not os.path.exists(letters_dir):
            os.mkdir(letters_dir)

        k = 0
        for images in letters:
            for i in range(self.cols):
                if ord(self.LETTER_NAMES[k]) in range(65, 91):
                    letter = letters_dir + "/" + 2 * self.LETTER_NAMES[k + 26]
                else:
                    letter = letters_dir + "/" + self.LETTER_NAMES[k]
                if not os.path.exists(letter):
                    os.mkdir(letter)
                cv2.imwrite(letter + "/" + self.LETTER_NAMES[k] + ".png", images[i][0])
                k += 1
                if k == 62:
                    break


if __name__ == "__main__":
    a = SheetToPNG(
        sheet_dir=os.getcwd() + "/sheets",
        letters_dir=os.path.dirname(os.getcwd()) + "/letters",
        cols=NUM,
        rows=9,
    )
