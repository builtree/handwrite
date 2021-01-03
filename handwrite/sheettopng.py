import os

import cv2

ASCII = list(map(chr, range(127)))
# Seq: A-Z, a-z, 0-9, punctuation
RANGES = [(65, 91), (97, 123), (48, 58)]


class SheetToPNG:
    LETTER_NAMES = [item for start, end in RANGES for item in ASCII[start:end]] + ["."]

    def __init__(self, sheet, letters_dir, cols, rows=9):
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
        letters = [[] for _ in range(self.rows)]

        sheet_area = image.shape[0] * image.shape[1]
        min_area = sheet_area / 110
        max_area = sheet_area / 90
        i = 0

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # blurred = cv2.medianBlur(gray, 3)

        # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1],])
        # filtered = cv2.filter2D(blurred, -1, kernel)

        ret, thresh = cv2.threshold(gray, 200, 255, 1)
        close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, close_kernel, iterations=2)

        contours, h = cv2.findContours(
            close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            area = cv2.contourArea(cnt)
            space = int(area ** 0.5 / 2.3)

            if len(approx) == 4 and min_area < area < max_area:
                x, y, w, h = cv2.boundingRect(cnt)
                cx, cy = x + w // 2, y + h // 2

                roi = image[cy - space : cy + space, cx - space : cx + space]
                letters[-1 - i // self.cols].append([roi, cx])
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
                    letter = os.path.join(letters_dir, 2 * self.LETTER_NAMES[k + 26])
                else:
                    letter = os.path.join(letters_dir, self.LETTER_NAMES[k])
                if not os.path.exists(letter):
                    os.mkdir(letter)
                cv2.imwrite(
                    os.path.join(letter, self.LETTER_NAMES[k] + ".png"), images[i][0]
                )
                k += 1
                if k == 62:
                    break


if __name__ == "__main__":
    directory = os.path.dirname(os.getcwd())
    a = SheetToPNG(
        sheet=os.path.join(directory, "sheets", "didi.jpg"),
        letters_dir=os.path.join(directory, "letters"),
        cols=7,
        rows=9,
    )
