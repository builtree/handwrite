import unittest
import tempfile
import shutil
import itertools
import os
import platform
import subprocess
from handwrite.sheettopng import SheetToPNG

SPECIAL_CHARS = [
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

ALL_CHARS = list(
    itertools.chain(
        range(65, 91), range(97, 123), range(48, 58), [ord(i) for i in SPECIAL_CHARS]
    )
)


class TestSheetToPNG(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.mkdtemp()
        self.sheets_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "test_data" + os.sep + "sheettopng",
        )
        self.converter = SheetToPNG()

    def tearDown(self):
        shutil.rmtree(self.directory)

    def test_convert(self):
        excellent_scan = os.path.join(self.sheets_path, "excellent.jpg")
        self.converter.convert(excellent_scan, self.directory)
        for i in ALL_CHARS:
            self.assertTrue(
                os.path.exists(
                    os.path.join(self.directory, f"{i}" + os.sep + f"{i}.png")
                )
            )

    # TODO Once all the errors are done for detectCharacters
    # Write tests to check each kind of scan and whether it raises
    # helpful errors, Boilerplate below:
    # def test_detectCharacters(self):
    #     scans = ["excellent", "good", "average"]
    #     for scan in scans:
    #         detected_chars = self.converter.detectCharacters(
    #             os.path.join(self.sheets_path, f"{scan}.jpg")
    #         )
