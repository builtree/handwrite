import os
import shutil
import tempfile
import unittest

from handwrite import SheetToPNG, SVGtoTTF, PngToSvg


class TestSVGtoTTF(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.mkdtemp()
        self.characters_dir = tempfile.mkdtemp(dir=self.temp)
        self.sheet_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test_data",
            "sheettopng",
            "excellent.jpg",
        )
        self.config = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test_data",
            "config_data",
            "default.json",
        )
        SheetToPNG().convert(self.sheet_path, self.characters_dir, self.config)
        PngToSvg().convert(directory=self.characters_dir)
        self.converter = SVGtoTTF()

    def tearDown(self):
        shutil.rmtree(self.temp)

    def test_convert(self):
        self.converter.convert(self.characters_dir, self.temp, self.config)
        self.assertTrue(os.path.exists(os.path.join(self.temp, "MyFont.ttf")))
        # os.remove(os.join())

    def test_convert_duplicate(self):
        fake_ttf = tempfile.NamedTemporaryFile(
            suffix=".ttf", dir=self.temp, delete=False
        )
        fake_ttf.close()  # Doesn't keep open
        os.rename(fake_ttf.name, os.path.join(self.temp, "MyFont.ttf"))
        self.converter.convert(self.characters_dir, self.temp, self.config)
        self.assertTrue(os.path.exists(os.path.join(self.temp, "MyFont-default.ttf")))
        self.converter.convert(self.characters_dir, self.temp, self.config)
        self.assertTrue(
            os.path.exists(os.path.join(self.temp, "MyFont-default (1).ttf"))
        )
