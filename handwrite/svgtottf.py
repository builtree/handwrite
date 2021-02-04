import sys
import os.path
import json
import subprocess

IMPORT_OPTIONS = ("removeoverlap", "correctdir")


class SVGtoTTF:
    def __init__(self):
        pass

    def convert(self, directory, outfile, config):
        if directory[-1] not in "\/":
            directory = directory + "/"
        subprocess.run(
            [
                "fontforge",
                "--script",
                os.path.realpath(__file__),
                config,
                directory,
                outfile,
            ]
        )


def loadConfig(filename="default"):
    if filename == "default":
        filename = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "default.json"
        )
    with open(filename) as f:
        return json.load(f)


def setProperties(font, config):
    props = config["props"]
    lang = props.pop("lang", "English (US)")
    family = props.get("filename", "Example")
    style = props.pop("style", "Regular")
    font.familyname = family
    font.fontname = family + "-" + style
    font.fullname = family + " " + style
    font.encoding = props.pop("encoding", "UnicodeFull")

    for k, v in props.items():
        if hasattr(font, k):
            if isinstance(v, list):
                v = tuple(v)
            setattr(font, k, v)

    for t in config.get("sfnt_names", []):
        font.appendSFNTName(str(lang), str(t[0]), str(t[1]))


def addGlyphs(font, config, unicode_mapping, directory):
    space = font.createMappedChar(ord(" "))
    space.width = 500

    for k in config["glyphs"]:
        g = font.createMappedChar(k)
        unicode_mapping.setdefault(k, g.glyphname)
        # Get outlines
        src = "{}/{}.svg".format(k, k)
        # if not isinstance(v, dict):
        v = {"src": src}
        # src = "%s%s%s" % (config.get("input", "."), os.path.sep, v.pop("src", src))
        src = "%s%s" % (directory, v.pop("src", src))
        g.importOutlines(src, IMPORT_OPTIONS)
        g.removeOverlap()
        # Copy attributes
        for k2, v2 in v.items():
            if hasattr(g, k2):
                if isinstance(v2, list):
                    v2 = tuple(v2)
                setattr(g, k2, v2)


def setBearings(font, bearings, unicode_mapping):
    default = bearings.pop("Default")

    for k, v in bearings.items():
        if v[0] == None:
            v[0] = default[0]
        if v[1] == None:
            v[1] = default[1]

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


def main(config_file, directory, outdir):
    config = loadConfig(config_file)
    font = fontforge.font()
    unicode_mapping = {}

    setProperties(font, config)
    addGlyphs(font, config, unicode_mapping, directory)

    # bearing table
    setBearings(
        font, config["typography_parameters"].get("bearing_table", {}), unicode_mapping
    )

    # kerning table
    setKerning(font, config["typography_parameters"].get("kerning_table", {}))

    # Generate font and save as a .ttf file
    outfile = outdir + os.sep + str(config["props"].get("filename", "Example"))
    outfile = outfile + ".ttf" if not outfile.endswith(".ttf") else outfile
    sys.stderr.write("\nGenerating %s...\n" % outfile)
    font.generate(outfile)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        sys.stderr.write(
            "\nUsage: %s something.json output_font_name.ttf" % sys.argv[0]
        )
