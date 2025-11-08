from __future__ import annotations
import argparse, csv, json
from pathlib import Path

VALID = {"broken_bone", "non_broken"}

def export(image_dir: str, label: str, out_csv: str) -> int:
    if label not in VALID:
        raise SystemExit(f"label must be one of {VALID}")
    rows = []
    p = Path(image_dir)
    for jf in p.glob("*.json"):
        data = json.loads(jf.read_text(encoding="utf-8"))
        img = jf.with_suffix(".jpg").name
        for det in data.get("Body", {}).get("detections", []):
            if det.get("label") == label:
                rows.append({
                    "image": img,
                    "label": det.get("label", ""),
                    "x0": det.get("x0", ""),
                    "y0": det.get("y0", ""),
                    "x1": det.get("x1", ""),
                    "y1": det.get("y1", ""),
                    "detectionBoxArea": det.get("detectionBoxArea", ""),
                    "detectionBoxDiagonal": det.get("detectionBoxDiagonal", "")
                })
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        if rows:
            headers = list(rows[0].keys())
        else:
            headers = ["image", "label", "x0", "y0", "x1", "y1", "detectionBoxArea", "detectionBoxDiagonal"]
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"[OK] exported {len(rows)} rows -> {out_csv}")
    return len(rows)

def cli():
    ap = argparse.ArgumentParser(description="Export labeled detections to CSV")
    ap.add_argument("--image-dir", required=True)
    ap.add_argument("--type", choices=["BB", "NB"], required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    label = "broken_bone" if args.type == "BB" else "non_broken"
    export(args.image_dir, label, args.out)

if __name__ == "__main__":
    cli()
