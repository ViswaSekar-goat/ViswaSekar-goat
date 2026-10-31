#!/usr/bin/env python3
"""Apply a restrained neon-arcade treatment to generated contribution-game SVGs."""
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

def tag(name):
    return f"{{{SVG_NS}}}{name}"

def neonize(path: Path) -> None:
    if not path.exists():
        return

    tree = ET.parse(path)
    root = tree.getroot()

    # Add reusable glow filters and a compact theme stylesheet.
    defs = root.find(tag("defs"))
    if defs is None:
        defs = ET.Element(tag("defs"))
        root.insert(0, defs)

    tile_filter = ET.SubElement(defs, tag("filter"), {
        "id": "neonTile", "x": "-80%", "y": "-80%",
        "width": "260%", "height": "260%"
    })
    ET.SubElement(tile_filter, tag("feGaussianBlur"), {
        "stdDeviation": "1.7", "result": "blur"
    })
    merge = ET.SubElement(tile_filter, tag("feMerge"))
    ET.SubElement(merge, tag("feMergeNode"), {"in": "blur"})
    ET.SubElement(merge, tag("feMergeNode"), {"in": "SourceGraphic"})

    sprite_filter = ET.SubElement(defs, tag("filter"), {
        "id": "neonSprite", "x": "-100%", "y": "-100%",
        "width": "300%", "height": "300%"
    })
    for color, deviation in (("#22d3ee", "3"), ("#a855f7", "7")):
        shadow = ET.SubElement(sprite_filter, tag("feDropShadow"), {
            "dx": "0", "dy": "0", "stdDeviation": deviation,
            "flood-color": color, "flood-opacity": "0.9"
        })

    style = ET.SubElement(defs, tag("style"))
    style.text = """
      svg { background: #070b16; }
      text { fill: #b8c7e0 !important; }
      rect { filter: url(#neonTile); }
      path, circle, ellipse, polygon { filter: url(#neonSprite); }
    """

    # Transparent SVGs render against the same deep navy arcade canvas in README.
    root.set("style", (root.get("style", "") + ";background:#070b16").strip(";"))

    # Keep the SVG compact and preserve its existing animation elements.
    tree.write(path, encoding="utf-8", xml_declaration=True)

def main():
    output_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    for svg in output_dir.glob("*.svg"):
        neonize(svg)
        print(f"Neon arcade styling applied: {svg}")

if __name__ == "__main__":
    main()
