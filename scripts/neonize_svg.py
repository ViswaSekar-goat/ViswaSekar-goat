from pathlib import Path
import sys
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)

def q(name):
    return f"{{{SVG}}}{name}"

def neonize(file):
    tree = ET.parse(file)
    root = tree.getroot()

    defs = root.find(q("defs"))
    if defs is None:
        defs = ET.SubElement(root, q("defs"))

    # Remove old filters/styles to prevent duplicate IDs.
    for element in list(defs):
        if element.get("id") in {"neonTile", "neonSprite", "neonGlow"}:
            defs.remove(element)
        elif element.tag == q("style"):
            defs.remove(element)

    glow = ET.SubElement(defs, q("filter"), {
        "id": "neonGlow",
        "x": "-100%", "y": "-100%",
        "width": "300%", "height": "300%",
        "color-interpolation-filters": "sRGB"
    })

    blur = ET.SubElement(glow, q("feGaussianBlur"), {
        "stdDeviation": "3",
        "result": "blur"
    })

    merge = ET.SubElement(glow, q("feMerge"))
    ET.SubElement(merge, q("feMergeNode"), {"in": "blur"})
    ET.SubElement(merge, q("feMergeNode"), {"in": "SourceGraphic"})

    # Neon theme and glow for actual Pac-Man sprites.
    style = ET.SubElement(defs, q("style"))
    style.text = """
    svg { background: #070b16; }
    text { fill: #a5b4fc !important; }

    #pacman, [id*="pacman"], [id*="ghost"] {
        filter: url(#neonGlow);
    }

    [id^="c-"] {
        stroke: #22d3ee;
        stroke-opacity: 0.35;
        stroke-width: 0.8;
    }

    [id^="c-"]:not([fill="#161b22"]) {
        filter: url(#neonGlow);
    }
    """

    root.set("style", "background:#070b16")

    tree.write(file, encoding="utf-8", xml_declaration=True)
    print(f"Neon styling applied: {file}")

def main():
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")

    for file in folder.glob("*.svg"):
        neonize(file)

if __name__ == "__main__":
    main()
