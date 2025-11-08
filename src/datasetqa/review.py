from __future__ import annotations
import argparse, json, os
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def review_folder(image_dir: str, default_type: str = "BB", overwrite: bool = False) -> None:
    image_dir = Path(image_dir)
    files = [f for f in os.listdir(image_dir) if f.lower().endswith((".jpg", ".png"))]
    files.sort()
    print(f"[INFO] Found {len(files)} images")

    for filename in files:
        img_path = image_dir / filename
        json_path = img_path.with_suffix(".json")
        if not json_path.exists():
            print(f"[WARN] missing JSON for {filename} – run prepare.py first. Skipping.")
            continue

        data = json.loads(json_path.read_text(encoding="utf-8"))
        dets = data.get("Body", {}).get("detections", [])
        if not dets:
            continue

        im = cv2.imread(str(img_path))
        if im is None:
            continue
        rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        fig, ax = plt.subplots(figsize=(10, 7))
        plt.subplots_adjust(bottom=0.2)
        ax.imshow(rgb)
        ax.axis("off")
        ax.set_title(f"Label image: {filename}")

        for d in dets:
            x0, y0, x1, y1 = int(d["x0"]), int(d["y0"]), int(d["x1"]), int(d["y1"])
            ax.add_patch(plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, linewidth=2))

        selected = {"value": None}

        def cb(val):
            def inner(_):
                selected["value"] = val
                plt.close(fig)
            return inner

        btn_w = 0.18
        y = 0.05
        x_positions = [0.1, 0.32, 0.54, 0.76]
        ax_bb = plt.axes([x_positions[0], y, btn_w, 0.075])
        ax_nb = plt.axes([x_positions[1], y, btn_w, 0.075])
        ax_ex = plt.axes([x_positions[2], y, btn_w, 0.075])
        ax_quit = plt.axes([x_positions[3], y, btn_w, 0.075])

        b1 = Button(ax_bb, "Broken bone")
        b2 = Button(ax_nb, "Non-broken")
        b3 = Button(ax_ex, "Exclude")
        b4 = Button(ax_quit, "Save and Quit")

        b1.on_clicked(cb("broken_bone"))
        b2.on_clicked(cb("non_broken"))
        b3.on_clicked(cb("excluded"))
        b4.on_clicked(cb("quit"))
        plt.show()

        if selected["value"] is None:
            continue
        if selected["value"] == "quit":
            print("[INFO] quitting review and saving progress")
            break

        for d in dets:
            x0, y0, x1, y1 = int(d["x0"]), int(d["y0"]), int(d["x1"]), int(d["y1"])
            w, h = abs(x1 - x0), abs(y1 - y0)
            d["detectionBoxArea"] = w * h
            d["detectionBoxDiagonal"] = (w * w + h * h) ** 0.5
            d["label"] = selected["value"]
        json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"[OK] {filename} -> label={selected['value']}")

def cli():
    ap = argparse.ArgumentParser(description="Visual review tool for broken vs non-broken labeling")
    ap.add_argument("--image-dir", required=True, help="Folder containing images + JSON")
    ap.add_argument("--type", choices=["BB", "NB"], default="BB")
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()
    review_folder(args.image_dir, default_type=args.type, overwrite=args.overwrite)

if __name__ == "__main__":
    cli()
