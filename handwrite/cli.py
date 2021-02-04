import shutil
import argparse
import tempfile

from handwrite import SheetToPNG
from handwrite import PngToSvg
from handwrite import SVGtoTTF


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sheet", help="Path to sample sheet")
    parser.add_argument("output", help="Directory Path to save font output")
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
    SVGtoTTF().convert(directory, args.output, args.config)

    if not args.directory:
        shutil.rmtree(directory)
