import sys
import shutil
import argparse
import tempfile
import subprocess

from handwrite.sheettopng import SheetToPNG
from handwrite.pngtosvg import PngToSvg
from handwrite.svgtottf import SVGtoTTF


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sheet", help="Path to sample sheet")
    parser.add_argument("output", help="Name of the font output")
    parser.add_argument(
        "--directory",
        help="Generate additional files to this path (Temp by default)",
        default=None,
    )
    parser.add_argument("--config", help="Use custom configuration", default="default")
    args = parser.parse_args()

    directory = args.directory
    if not directory:
        directory = tempfile.mkdtemp()

    SheetToPNG().convert(args.sheet, directory)
    PngToSvg().convert(directory=directory)
    SVGtoTTF().convert(directory, args.output + ".ttf", args.config)

    if not args.directory:
        shutil.rmtree(directory)
