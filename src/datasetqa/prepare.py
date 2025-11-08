from __future__ import annotations
import argparse, json
from pathlib import Path
from PIL import Image

def make_json_for_folder(image_dir: str) -> int:
    p = Path(image_dir)
    if not p.exists():
        raise SystemExit(f"[ERROR] folder not found: {image_dir}")
    count = 0
    for img_path in list(p.glob("*.jpg")) + list(p.glob("*.png")):
        try:
            im = Image.open(img_path)
            w, h = im.size
        except Exception:
            continue
        data = {
            "Body": {"detections": [{"x0": 0, "y0": 0, "x1": w - 1, "y1": h - 1, "label": ""}]}
        }
        json_path = img_path.with_suffix(".json")
        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        count += 1
    return count

def cli():
    ap = argparse.ArgumentParser(description="Create per-image JSON with full-frame detection for quick review.")
    ap.add_argument("--image-dir", required=True, help="Folder containing images")
    args = ap.parse_args()
    n = make_json_for_folder(args.image_dir)
    print(f"Prepared {n} JSON files in {args.image_dir}")

if __name__ == "__main__":
    cli()
