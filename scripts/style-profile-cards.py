"""Apply the website palette to generated cards, preserving their data and geometry."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CARDS = ("0-profile-details.svg", "1-repos-per-language.svg", "3-stats.svg")
PALETTES = {
    "light": {"#ffffff": "#faf9f7", "#e4e2e2": "#ded9e1", "#0366d6": "#794590", "#586069": "#484653", "#40c463": "#a18bad", "#3572a5": "#8d9db5", "#e34c26": "#bea1b5"},
    "dark": {"#ffffff": "#211f27", "#e4e2e2": "#413b49", "#0366d6": "#c6a7d5", "#586069": "#d3ced8", "#40c463": "#a38dbb", "#3572a5": "#94a7c4", "#e34c26": "#c5a3b9"},
}

for theme, palette in PALETTES.items():
    output = ROOT / "assets" / "profile" / theme
    output.mkdir(parents=True, exist_ok=True)
    for filename in CARDS:
        original = (ROOT / "profile-summary-card-output" / "github" / filename).read_text()
        styled = re.sub(r"#[0-9a-fA-F]{6}\b", lambda m: palette.get(m[0].lower(), m[0]), original)
        before, after = ET.fromstring(original), ET.fromstring(styled)
        ns = {"s": "http://www.w3.org/2000/svg"}
        assert [e.text for e in before.findall('.//s:text', ns)] == [e.text for e in after.findall('.//s:text', ns)]
        assert [e.get('d') for e in before.findall('.//s:path', ns)] == [e.get('d') for e in after.findall('.//s:path', ns)]
        (output / filename).write_text(styled)
print("Styled 3 data-preserving cards in light and dark palettes.")
