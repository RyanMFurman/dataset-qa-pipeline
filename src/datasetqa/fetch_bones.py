from __future__ import annotations
import argparse, json
from pathlib import Path

def fetch_mura(out_dir: str, limit: int | None = None) -> int:
    try:
        from datasets import load_dataset
    except Exception:
        raise SystemExit(
            "\n[ERROR] 'datasets' is required. Install with: pip install datasets huggingface_hub\n"
        )
    ds = load_dataset("KhalfounMehdi/MURA", split="train")
    out = Path(out_dir)
    (out / "broken_bone").mkdir(parents=True, exist_ok=True)
    (out / "non_broken").mkdir(parents=True, exist_ok=True)
    from PIL import Image
    saved = 0
    for i, row in enumerate(ds):
        if limit is not None and saved >= limit:
            break
        pil = row.get("image")
        label_text = str(row.get("label_text") or row.get("label")).lower()
        if pil is None or label_text is None:
            continue
        target = (
            "broken_bone"
            if ("abnormal" in label_text or label_text == "1")
            else ("non_broken" if ("normal" in label_text or label_text == "0") else None)
        )
        if target is None:
            continue
        sub = out / target
        fname = f"mura_{i:06d}.jpg"
        save_path = sub / fname
        pil.convert("RGB").save(save_path, "JPEG", quality=95)
        w, h = pil.size
        data = {
            "Body": {"detections": [{"x0": 0, "y0": 0, "x1": w - 1, "y1": h - 1, "label": ""}]}
        }
        save_path.with_suffix(".json").write_text(json.dumps(data, indent=2), encoding="utf-8")
        saved += 1
    return saved

def cli():
    ap = argparse.ArgumentParser(description="Fetch real X-rays and prep JSONs (MURA mirror)")
    ap.add_argument("--source", choices=["mura"], default="mura")
    ap.add_argument("--out-dir", default="./examples/bones_real")
    ap.add_argument("--max", type=int, default=200)
    args = ap.parse_args()
    if args.source == "mura":
        n = fetch_mura(args.out_dir, args.max)
        print(f"Downloaded and prepared {n} images into '{args.out_dir}'.")

if __name__ == "__main__":
    cli()
