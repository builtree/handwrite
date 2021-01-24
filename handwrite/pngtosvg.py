from PIL import Image, ImageChops
import os
import subprocess


class PngToSvg:
    def __init__(self, directory=None, font_name="", config={}):
        path = os.walk(directory)
        for root, dirs, files in path:
            for f in files:
                if f[-4:] == ".png":
                    self.pngToBmp(root + "/" + f)
                    # self.trim(root + "/" + f[0:-4] + ".bmp")
                    self.bmpToSvg(root + "/" + f[0:-4] + ".bmp")

    def bmpToSvg(self, path):
        subprocess.run(["potrace", path, "-b", "svg", "-o", path[0:-4] + ".svg"])

    def pngToBmp(self, path):
        png = Image.open(path)
        img = png.convert("RGBA")
        # Resizing char images to default size
        img = img.resize((100, 100))
        data = list(img.getdata())
        threshold = 200
        newdata = []
        for pix in data:
            if pix[0] >= threshold and pix[1] >= threshold and pix[3] >= threshold:
                newdata.append((255, 255, 255, 0))
            else:
                newdata.append((0, 0, 0, 1))
        img.putdata(newdata)
        img.save(path[0:-4] + ".bmp")

    def trim(self, im_path):
        im = Image.open(im_path)
        bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))
        diff = ImageChops.difference(im, bg)
        bbox = list(diff.getbbox())
        bbox[0] -= 1
        bbox[1] -= 1
        bbox[2] += 1
        bbox[3] += 1
        cropped_im = im.crop(bbox)
        cropped_im.save(im_path)


if __name__ == "__main__":
    a = PicturesToFont(directory=os.path.dirname(os.getcwd()) + "/letters")
