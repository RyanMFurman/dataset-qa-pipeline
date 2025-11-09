 Dataset QA Toolkit — X-ray Image Labeling & Export

A neutral, open-source toolkit to inspect and QA image detections and export annotations to CSV for downstream analytics or model training.
This version is domain-agnostic but uses broken-bone vs. non-broken X-ray classification as its demonstration case.

Overview
Tool	Purpose
datasetqa-review	Interactive visual review of image + JSON pairs — add human labels and computed box metrics
datasetqa-export	Filter reviewed detections and export a clean CSV
datasetqa-makejson	Auto-generate placeholder JSONs for any folder of images
datasetqa-fetch-bones	Download real X-ray data (MURA) and prepare JSONs automatically

All names are generic — no proprietary or company-specific terms.
 Quickstart
pip install -e .
# Launch interactive review (choose Broken bone / Non-broken / Exclude)
datasetqa-review --image-dir ./examples/bones_demo --type BB --overwrite

# Export reviewed detections to CSV
datasetqa-export --image-dir ./examples/bones_demo --type BB --out detections.csv

Label Keys
Code	Label	Meaning
BB	broken_bone	Fractured / abnormal X-ray
NB	non_broken	Healthy / normal X-ray
EX	excluded	Skipped or not relevant
📄 JSON Schema

Each image (.jpg or .png) has a matching .json:

{
  "Body": {
    "detections": [
      {
        "x0": 10,
        "y0": 20,
        "x1": 100,
        "y1": 120,
        "label": ""
      }
    ]
  }
}


During review, the tool adds:

label → "broken_bone", "non_broken", or "excluded"

detectionBoxArea → box area (int)

detectionBoxDiagonal → diagonal length (float)

Example Workflow
Create JSONs for your own images
datasetqa-makejson --image-dir ./data/broken_bone
datasetqa-makejson --image-dir ./data/non_broken

Run the reviewer
datasetqa-review --image-dir ./data/broken_bone --type BB --overwrite
datasetqa-review --image-dir ./data/non_broken --type NB --overwrite

Export to CSV
datasetqa-export --image-dir ./data/broken_bone --type BB --out bones_bb.csv
datasetqa-export --image-dir ./data/non_broken --type NB --out bones_nb.csv

 Fetch Real X-rays (MURA via Hugging Face)

Install extras:

pip install datasets huggingface_hub


Fetch and prep automatically:

datasetqa-fetch-bones --source mura --out-dir ./examples/bones_real --max 60


Then review and export:

python -m datasetqa.review --image-dir ./examples/bones_real/broken_bone --type BB --overwrite
python -m datasetqa.review --image-dir ./examples/bones_real/non_broken --type NB --overwrite
datasetqa-export --image-dir ./examples/bones_real/broken_bone --type BB --out bones_real_bb.csv
datasetqa-export --image-dir ./examples/bones_real/non_broken --type NB --out bones_real_nb.csv

Docker Quickstart

Build and launch inside a container:

docker build -t datasetqa:latest .
docker run --rm -it -p 8888:8888 -v "$PWD":/app datasetqa:latest bash


Inside the container:

datasetqa-fetch-bones --source mura --out-dir ./examples/bones_real --max 60
python -m datasetqa.review --image-dir ./examples/bones_real/broken_bone --type BB
python -m datasetqa.export --image-dir ./examples/bones_real/broken_bone --type BB --out bones_real_bb.csv

Jupyter Notebook Demo

The included notebook notebooks/bones_baseline.ipynb demonstrates:

Loading labeled X-ray data

Preprocessing and normalization

Training a baseline logistic-regression model

Plotting confusion matrix & sample predictions

Run in VS Code:

Open the notebook

Select your .venv Python 3.11 kernel

Click Run All


MIT License © 2025 Ryan Furman
Free for research and educational use.
