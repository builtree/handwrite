import sys
import os.path
import json

IMPORT_OPTIONS = ("removeoverlap", "correctdir")

try:
    unicode
except NameError:
    unicode = str


def loadConfig(filename="font.json"):
    with open(filename) as f:
        return json.load(f)


def setProperties(font, config):
    props = config["props"]
    lang = props.pop("lang", "English (US)")
    family = props.pop("family", None)
    style = props.pop("style", "Regular")
    props["encoding"] = props.get("encoding", "UnicodeFull")
    if family is not None:
        font.familyname = family
        font.fontname = family + "-" + style
        font.fullname = family + " " + style
    for k, v in config["props"].items():
        if hasattr(font, k):
            if isinstance(v, list):
                v = tuple(v)
            setattr(font, k, v)
        else:
            font.appendSFNTName(lang, k, v)
    for t in config.get("sfnt_names", []):
        font.appendSFNTName(str(t[0]), str(t[1]), unicode(t[2]))


def addGlyphs(font, config):
    space = font.createMappedChar(ord(" "))
    space.width = 1000

    for k, v in config["glyphs"].items():
        g = font.createMappedChar(ord(k))
        # Get outlines
        src = "%s.svg" % k
        if not isinstance(v, dict):
            v = {"src": v or src}
        src = "%s%s%s" % (config.get("input", "."), os.path.sep, v.pop("src", src))
        g.importOutlines(src, IMPORT_OPTIONS)
        g.removeOverlap()
        # Copy attributes
        for k2, v2 in v.items():
            if hasattr(g, k2):
                if isinstance(v2, list):
                    v2 = tuple(v2)
                setattr(g, k2, v2)


def setBearings(font, bearings):
    default = bearings.pop("Default")

    for k, v in bearings.items():
        if v[0] == None:
            v[0] = default[0]
        if v[1] == None:
            v[1] = default[1]

        font[k].left_side_bearing = v[0]
        font[k].right_side_bearing = v[1]


def setKerning(font, table):
    rows = table["rows"]
    rows = [list(i) if i != None else None for i in rows]
    cols = table["cols"]
    cols = [list(i) if i != None else None for i in cols]

    kerning_table = table["table"]
    flatten_list = (
        lambda y: [x for a in y for x in flatten_list(a)] if type(y) is list else [y]
    )
    kerning_list = [0 if x == None else x for x in flatten_list(kerning_table)]

    font.addLookup("kern", "gpos_pair", 0, [["kern", [["latn", ["dflt"]]]]])
    font.addKerningClass("kern", "kern-1", 0, rows, cols, True)
    # font.autoKern("kern-1", 0, rows, cols)
    # print(font.getKerningClass("kern-1"))


def main(config_file):
    config = loadConfig(config_file)
    os.chdir(os.path.dirname(config_file) or ".")
    font = fontforge.font()
    setProperties(font, config)
    addGlyphs(font, config)

    # bearing table
    setBearings(font, config.get("bearing_table", {}))

    # kerning table
    setKerning(font, config.get("kerning_table", {}))

    for outfile in config["output"]:
    sys.stderr.write("Generating %s...\n" % outfile)
    font.generate(outfile)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        sys.stderr.write("\nUsage: %s something.json\n" % sys.argv[0])
