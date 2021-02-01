import os
import unittest

from handwrite.pngtosvg import PngToSvg


class TestPngToSvg(unittest.TestCase):
    def setUp(self):
        self.directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test_data" + os.sep + "pngtosvg",
        )
        self.converter = PngToSvg()

    def test_bmpToSvg(self):
        self.converter.bmpToSvg(self.directory + os.sep + "45.bmp")
        self.assertTrue(os.path.exists(self.directory + os.sep + "45.svg"))
        os.remove(self.directory + os.sep + "45.svg")

    def test_convert(self):
        self.converter.convert(self.directory)
        path = os.walk(self.directory)
        for root, dirs, files in path:
            for f in files:
                if f[-4:] == ".png":
                    self.assertTrue(os.path.exists(root + os.sep + f[0:-4] + ".bmp"))
                    self.assertTrue(os.path.exists(root + os.sep + f[0:-4] + ".svg"))
                    os.remove(root + os.sep + f[0:-4] + ".bmp")
                    os.remove(root + os.sep + f[0:-4] + ".svg")
