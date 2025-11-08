#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Installing package (editable) ==="
pip install -e .

echo "=== Installing data deps (Hugging Face) ==="
pip install datasets huggingface_hub opencv-python matplotlib

echo "=== Fetching real X-rays (FracAtlas) ==="
datasetqa-fetch-bones --out-dir ./examples/bones_real --max 60

echo "=== Review: broken ==="
python -m datasetqa.review --image-dir ./examples/bones_real/broken_bone --type BB --overwrite

echo "=== Review: non-broken ==="
python -m datasetqa.review --image-dir ./examples/bones_real/non_broken --type NB --overwrite

echo "=== Export CSVs ==="
datasetqa-export --image-dir ./examples/bones_real/broken_bone --type BB --out bones_real_bb.csv
datasetqa-export --image-dir ./examples/bones_real/non_broken --type NB --out bones_real_nb.csv

echo "Done. CSVs are in the project root."