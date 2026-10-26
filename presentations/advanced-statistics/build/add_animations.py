"""Adds native PowerPoint transitions and click-reveal animations to the built deck.

pptxgenjs cannot write animations, so this post-processes the slide XML:
  * every slide gets a medium-speed Fade transition;
  * shapes whose name ends in " #n" fade in together on click n (the suffix is removed).

Usage: python3 add_animations.py deck.pptx
"""
import re
import sys
import zipfile

from lxml import etree

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
}
P = "{%s}" % NS["p"]
TAG = re.compile(r"^(.*?) #(\d+)$")
FADE_MS = 500


def effect(ctn_id, spid, node_type):
    """One fade-in entrance effect (preset 10) for one shape."""
    return f"""<p:par><p:cTn id="{ctn_id}" presetID="10" presetClass="entr" presetSubtype="0" fill="hold" grpId="0" nodeType="{node_type}">
<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
<p:set><p:cBhvr><p:cTn id="{ctn_id + 1}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>
<p:to><p:strVal val="visible"/></p:to></p:set>
<p:animEffect transition="in" filter="fade"><p:cBhvr><p:cTn id="{ctn_id + 2}" dur="{FADE_MS}"/>
<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>
</p:childTnLst></p:cTn></p:par>"""


def timing_xml(steps, kinds):
    """steps: list of shape-id lists, one per click. kinds: spid -> 'sp' | 'graphicFrame' | 'pic'."""
    next_id = 3
    clicks = []
    for ids in steps:
        outer, inner = next_id, next_id + 1
        next_id += 2
        effects = []
        for k, spid in enumerate(ids):
            effects.append(effect(next_id, spid, "clickEffect" if k == 0 else "withEffect"))
            next_id += 3
        clicks.append(
            f'<p:par><p:cTn id="{outer}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>'
            f'<p:par><p:cTn id="{inner}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            + "".join(effects)
            + "</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>"
        )
    builds = []
    for ids in steps:
        for spid in ids:
            if kinds[spid] == "sp":
                builds.append(f'<p:bldP spid="{spid}" grpId="0" animBg="1"/>')
            elif kinds[spid] == "graphicFrame":
                builds.append(f'<p:bldGraphic spid="{spid}" grpId="0"><p:bldAsOne/></p:bldGraphic>')
    return (
        f'<p:timing xmlns:p="{NS["p"]}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
        '<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
        + "".join(clicks)
        + "</p:childTnLst></p:cTn>"
        '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
        '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
        "</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>"
        + (f"<p:bldLst>{''.join(builds)}</p:bldLst>" if builds else "")
        + "</p:timing>"
    )


def process_slide(xml):
    root = etree.fromstring(xml)
    groups, kinds = {}, {}
    for c in root.iter(P + "cNvPr"):
        m = TAG.match(c.get("name", ""))
        if not m:
            continue
        c.set("name", m.group(1))
        spid = c.get("id")
        groups.setdefault(int(m.group(2)), []).append(spid)
        kinds[spid] = etree.QName(c.getparent().getparent()).localname
    for old in root.findall("p:transition", NS) + root.findall("p:timing", NS):
        root.remove(old)
    anchor = root.find("p:clrMapOvr", NS)
    if anchor is None:
        anchor = root.find("p:cSld", NS)
    pos = list(root).index(anchor) + 1
    transition = etree.fromstring(f'<p:transition xmlns:p="{NS["p"]}" spd="med"><p:fade/></p:transition>')
    root.insert(pos, transition)
    if groups:
        root.insert(pos + 1, etree.fromstring(timing_xml([groups[k] for k in sorted(groups)], kinds)))
    clicks = len(groups)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True), clicks


def main(path):
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    report = {}
    with zipfile.ZipFile(path + ".tmp", "w", zipfile.ZIP_DEFLATED) as out:
        for info, data in items:
            if re.match(r"ppt/slides/slide\d+\.xml$", info.filename):
                data, clicks = process_slide(data)
                report[info.filename] = clicks
            out.writestr(info, data)
    import os
    os.replace(path + ".tmp", path)
    for k in sorted(report, key=lambda s: int(re.findall(r"\d+", s)[0])):
        print(f"{k}: fade transition, {report[k]} click reveal(s)")


if __name__ == "__main__":
    main(sys.argv[1])
