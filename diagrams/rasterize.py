"""Rasterize SVG diagrams to PNG at 2x scale using headless Edge."""
import glob, os, re, subprocess

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
HERE = os.path.dirname(os.path.abspath(__file__))
PNG_DIR = os.path.join(HERE, "png")
os.makedirs(PNG_DIR, exist_ok=True)

for svg in sorted(glob.glob(os.path.join(HERE, "*.svg"))):
    with open(svg, encoding="utf-8") as f:
        head = f.read(300)
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', head)
    w, h = int(m.group(1)) * 2, int(m.group(2)) * 2
    out = os.path.join(PNG_DIR, os.path.basename(svg).replace(".svg", ".png"))
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--hide-scrollbars",
                    f"--screenshot={out}", f"--window-size={w},{h}",
                    "file:///" + svg.replace("\\", "/")],
                   check=True, capture_output=True, timeout=60)
    print("ok", os.path.basename(out))
print("done")
