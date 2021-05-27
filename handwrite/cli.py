import os
import shutil
import argparse
import tempfile

from handwrite import SHEETtoPNG
from handwrite import PNGtoSVG
from handwrite import SVGtoTTF


def run(sheet, output_directory, characters_dir, config):
    SHEETtoPNG().convert(sheet, characters_dir, config)
    PNGtoSVG().convert(directory=characters_dir)
    SVGtoTTF().convert(characters_dir, output_directory, config)


def converters(sheet, output_directory, directory=None, config=None):
    if not directory:
        directory = tempfile.mkdtemp()
        isTempdir = True
    else:
        isTempdir = False

    default_config = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "default.json"
    )
    if config is None:
        config = default_config

    configs_dir = None
    if os.path.isdir(config):
        configs_dir = config

    if os.path.isdir(sheet):
        configs_dir = configs_dir or directory + os.sep + "configs"
        os.makedirs(configs_dir, exist_ok=True)

        for sheet_name in sorted(os.listdir(sheet)):
            config_file = (
                configs_dir + os.sep + os.path.splitext(sheet_name)[0] + ".json"
            )
            if not os.path.exists(config_file):
                if os.path.isdir(config):
                    shutil.copyfile(default_config, config_file)
                else:
                    shutil.copyfile(config, config_file)

            characters_dir = directory + os.sep + os.path.splitext(sheet_name)[0]
            os.makedirs(characters_dir, exist_ok=True)
            run(
                sheet + os.sep + sheet_name,
                output_directory,
                characters_dir,
                config_file,
            )
    else:
        run(sheet, output_directory, directory, config)

    if isTempdir:
        shutil.rmtree(directory)


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
    converters(args.input_path, args.output_directory, args.directory, args.config)
