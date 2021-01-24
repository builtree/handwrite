import sys
import subprocess
from handwrite.sheettopng import SheetToPNG
from handwrite.pngtosvg import PngToSvg

# Temporary Function to call svgtottf with fontforge
def svgToTtf(directory, outfile):
    if directory[-1] not in "\/":
        directory = directory + "/"
    subprocess.run(
        [
            "fontforge",
            "--script",
            "handwrite/svgtottf.py",
            "handwrite/temp_config.json",
            directory,
            outfile,
        ]
    )


def main():
    args = sys.argv
    if len(args) > 1:
        # print(type(args[1]))
        SheetToPNG(args[1], letters_dir=args[2], cols=7)
        PngToSvg(directory=args[2])
        svgToTtf(args[2], args[3])
    else:
        print(
            "Usage: handwrite [PATH TO INITIAL SHEET] [DIRECTORY FOR SAVING TEMP IMAGES] [OUTPUT FONT NAME.ttf]"
        )
