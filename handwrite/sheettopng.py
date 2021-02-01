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
    CHARACTER_NAMES = [
        item for start, end in RANGES for item in ASCII[start:end]
    ] + SPECIAL_CHARACTERS

    def __init__(self):
        pass

    def convert(self, sheet, characters_dir, cols=8, rows=10):

        # TODO If directory given instead of image file, read all images and wrtie the images
        # (example) 0.png, 1.png, 2.png inside every character folder in characters/

        # sheet_images = []
        # for s in os.listdir(sheet_dir):
        #     sheet_images.append(cv2.imread(sheet_dir + "/" + s))

        characters = self.detectCharacters(sheet, cols=cols, rows=rows)
        self.createCharacterDirectory(characters, characters_dir)

    def detectCharacters(self, sheet_image, cols=8, rows=10):

        # TODO Raise errors and suggest where the problem might be

        # Read the image and convert to grayscale
        image = cv2.imread(sheet_image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Threshold and filter the image for better contour detection
        ret, thresh = cv2.threshold(gray, 200, 255, 1)
        close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, close_kernel, iterations=2)

        # Search for contours.
        contours, h = cv2.findContours(
            close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Filter contours based on number of sides and then reverse sort by area.
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

        # Calculate the bounding of the first contour and approximate the height
        # and width for final cropping.
        x, y, w, h = cv2.boundingRect(contours[0])
        space_h, space_w = 7 * h // 16, 7 * w // 16

        # Since amongst all the contours, the expected case is that the 4 sided contours
        # containing the characters should have the maximum area, so we loop through the first
        # rows*colums contours and add them to final list after cropping.
        characters = []
        for i in range(rows * cols):
            x, y, w, h = cv2.boundingRect(contours[i])
            cx, cy = x + w // 2, y + h // 2

            roi = image[cy - space_h : cy + space_h, cx - space_w : cx + space_w]
            characters.append([roi, cx, cy])

        # Now we have the characters but since they are all mixed up we need to position them.
        # Sort characters based on 'y' coordinate and group them by number of rows at a time. Then
        # sort each group based on the 'x' coordinate.
        characters.sort(key=lambda x: x[2])
        sorted_characters = []
        for k in range(rows):
            sorted_characters.extend(
                sorted(characters[cols * k : cols * (k + 1)], key=lambda x: x[1])
            )

        return sorted_characters

    def createCharacterDirectory(self, characters, characters_dir):
        if not os.path.exists(characters_dir):
            os.mkdir(characters_dir)

        # Create directory for each character and save the png for the characters
        # Structure: UserProvidedDir/ord(character)/ord(character).png
        for k, images in enumerate(characters):
            character = os.path.join(characters_dir, str(ord(self.CHARACTER_NAMES[k])))
            if not os.path.exists(character):
                os.mkdir(character)
            cv2.imwrite(
                os.path.join(character, str(ord(self.CHARACTER_NAMES[k])) + ".png"),
                images[0],
            )


def main():
    if len(sys.argv) > 1:
        a = SheetToPNG().convert(
            sheet=sys.argv[1],
            characters_dir=sys.argv[2],
            cols=8,
            rows=10,
        )
    else:
        print("Usage: sheettopng [SHEET_PATH] [CHARACTER_DIRECTORY_PATH]")
