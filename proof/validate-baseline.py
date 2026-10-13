import sys
import xml.etree.ElementTree as ET
root=ET.parse(sys.argv[1]).getroot()
cases=root.findall(".//testcase")
assert len(cases)==2
names={"native SVG cubic between fixed samples roots an attached line", "native SVG quadratic between fixed samples roots an attached line"}
assert {c.get("name") for c in cases} == names
for case in cases:
    failures=case.findall("failure")
    assert len(failures)==1 and not case.findall("error") and not case.findall("skipped")
    text=" ".join(failures[0].itertext())
    assert "eval: true" in text and "line ends: 1 of 1" in text and "native audit exit expected 0 received 1" in text
print("Verified two actual native curve attachment audit failures")
