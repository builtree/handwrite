import sys
import os.path
import json
import subprocess

IMPORT_OPTIONS = ("removeoverlap", "correctdir")


class SVGtoTTF:
    def convert(self, directory, outdir, config, sheet):
        subprocess.run(
            [
                "fontforge",
                "--script",
                os.path.realpath(__file__),
                config,
                directory,
                outdir,
                sheet,
            ]
        )


def loadConfig(filename="default"):
    if filename in ["default", "default_multiple"]:
        filename = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), filename + ".json"
        )
    with open(filename) as f:
        return json.load(f)


def setProperties(font, config, index):
    props = config["props"]
    lang = props.get("lang", "English (US)")
    family = props.get("filename", "Example")
    style = props.get("style", "Regular")
    if isinstance(family, list):
        family = family[index]
    if isinstance(style, list):
        style = style[index]

    font.familyname = family
    font.fontname = family + "-" + style
    font.fullname = family + " " + style
    font.encoding = props.get("encoding", "UnicodeFull")

    for k, v in props.items():
        if hasattr(font, k):
            if isinstance(v, list):
                v = tuple(v)
            setattr(font, k, v)

    for k, v in config.get("sfnt_names", {}).items():
        if isinstance(v, list):
            v = v[index]
        font.appendSFNTName(str(lang), str(k), str(v))


def addGlyphs(font, config, unicode_mapping, directory):
    space = font.createMappedChar(ord(" "))
    space.width = 500

    for k in config["glyphs"]:
        # Create character glyph
        g = font.createMappedChar(k)
        unicode_mapping.setdefault(k, g.glyphname)
        # Get outlines
        src = "{}/{}.svg".format(k, k)
        src = directory + os.sep + src
        g.importOutlines(src, IMPORT_OPTIONS)
        g.removeOverlap()


def setBearings(font, bearings, unicode_mapping):
    default = bearings.get("Default", [60, 60])

    for k, v in bearings.items():
        if v[0] == None:
            v[0] = default[0]
        if v[1] == None:
            v[1] = default[1]

        if k != "Default":
            glyph_name = unicode_mapping[ord(str(k))]
            font[glyph_name].left_side_bearing = v[0]
            font[glyph_name].right_side_bearing = v[1]


def setKerning(font, table):
    rows = table["rows"]
    rows = [list(i) if i != None else None for i in rows]
    cols = table["cols"]
    cols = [list(i) if i != None else None for i in cols]

    # kerning_table = table["table"]
    # flatten_list = (
    #     lambda y: [x for a in y for x in flatten_list(a)] if type(y) is list else [y]
    # )
    # kerning_list = [0 if x == None else x for x in flatten_list(kerning_table)]

    font.addLookup("kern", "gpos_pair", 0, [["kern", [["latn", ["dflt"]]]]])
    font.addKerningClass("kern", "kern-1", 0, rows, cols, True)
    # font.autoKern("kern-1", 0, rows, cols)
    # print(font.getKerningClass("kern-1"))


def generateFont(config, directory, outdir, index=0):
    font = fontforge.font()
    unicode_mapping = {}

    setProperties(font, config, index)
    addGlyphs(font, config, unicode_mapping, directory)

    # bearing table
    setBearings(
        font, config["typography_parameters"].get("bearing_table", {}), unicode_mapping
    )

    # kerning table
    setKerning(font, config["typography_parameters"].get("kerning_table", {}))

    # Generate font and save as a .ttf file
    filename = config["props"].get("filename", None)
    if filename is None:
        raise NameError("filename not found in config file.")
    elif isinstance(filename, list):
        filename = filename[index]

    outfile = outdir + os.sep + str(filename)
    outfile = outfile + ".ttf" if not outfile.endswith(".ttf") else outfile
    sys.stderr.write("\nGenerating %s...\n" % outfile)
    font.generate(outfile)


def main(config_file, directory, outdir, sheet):
    config = loadConfig(config_file)

    if os.path.isdir(sheet):
        for index, sheet_name in enumerate(os.listdir(sheet)):
            characters_dir = directory + os.sep + os.path.splitext(sheet_name)[0]
            generateFont(config, characters_dir, outdir, index)
    else:
        generateFont(config, directory, outdir)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        sys.stderr.write(
            "\nUsage: %s something.json output_font_name.ttf" % sys.argv[0]
        )
