import os
import shutil
import argparse
import tempfile

from handwrite import SheetToPNG
from handwrite import PngToSvg
from handwrite import SVGtoTTF


def converters(sheet, characters_dir, output_directory, config):
    SheetToPNG().convert(sheet, characters_dir, config)
    PngToSvg().convert(directory=characters_dir)
    SVGtoTTF().convert(characters_dir, output_directory, config)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_path", help="Path to sample sheet/directory with multiple sample sheets"
    )
    parser.add_argument("output_directory", help="Directory Path to save font output")
    parser.add_argument(
        "--directory",
        help="Generate additional files to this path (Temp by default)",
        default=None,
    )
    parser.add_argument(
        "--config", help="Use custom configuration file/directory", default=None
    )
    args = parser.parse_args()

    directory = args.directory
    if not directory:
        directory = tempfile.mkdtemp()

    default_config = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "default.json"
    )
    if args.config is None:
        args.config = default_config

    configs_dir = None
    if os.path.isdir(args.config):
        configs_dir = args.config

    if os.path.isdir(args.input_path):
        configs_dir = configs_dir or directory + os.sep + "configs"
        os.makedirs(configs_dir, exist_ok=True)

        for sheet_name in sorted(os.listdir(args.input_path)):
            config_file = (
                configs_dir + os.sep + os.path.splitext(sheet_name)[0] + ".json"
            )
            if not os.path.exists(config_file):
                if os.path.isdir(args.config):
                    shutil.copyfile(default_config, config_file)
                else:
                    shutil.copyfile(args.config, config_file)

            characters_dir = directory + os.sep + os.path.splitext(sheet_name)[0]
            os.makedirs(characters_dir, exist_ok=True)

            converters(
                args.input_path + os.sep + sheet_name,
                characters_dir,
                args.output_directory,
                config_file,
            )
    else:
        converters(args.input_path, directory, args.output_directory, args.config)

    if not args.directory:
        shutil.rmtree(directory)
