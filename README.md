Dataset QA Toolkit — X-ray Image Labeling & Export

An open-source toolkit for reviewing image detections, labeling data, and exporting annotations to CSV for analysis or model training.
This demo uses broken-bone vs. non-broken X-ray classification as an example.

Overview
Tool	Purpose
datasetqa-review	Interactive image and JSON review to add human labels
datasetqa-export	Filter and export reviewed detections to a clean CSV
datasetqa-makejson	Auto-generate placeholder JSONs for any image folder
datasetqa-fetch-bones	Download real X-rays (MURA dataset) and prepare JSONs

All tools use generic, non-proprietary names.

Quickstart
pip install -e .


Review and Label

datasetqa-review --image-dir ./examples/bones_demo --type BB --overwrite


Export to CSV

datasetqa-export --image-dir ./examples/bones_demo --type BB --out detections.csv

Label Keys
Code	Label	Meaning
BB	broken_bone	Fractured or abnormal X-ray
NB	non_broken	Healthy or normal X-ray
EX	excluded	Skipped or irrelevant image
JSON Format

Each image (.jpg or .png) has a matching .json file:

{
  "Body": {
    "detections": [
      {"x0": 10, "y0": 20, "x1": 100, "y1": 120, "label": ""}
    ]
  }
}


After review, the tool adds:

label: "broken_bone", "non_broken", or "excluded"

detectionBoxArea: integer area

detectionBoxDiagonal: diagonal length

Example Workflow

1. Create JSONs for your images

datasetqa-makejson --image-dir ./data/broken_bone
datasetqa-makejson --image-dir ./data/non_broken


2. Review and label

datasetqa-review --image-dir ./data/broken_bone --type BB --overwrite
datasetqa-review --image-dir ./data/non_broken --type NB --overwrite


3. Export to CSV

datasetqa-export --image-dir ./data/broken_bone --type BB --out bones_bb.csv
datasetqa-export --image-dir ./data/non_broken --type NB --out bones_nb.csv

Fetch Real X-rays (MURA via Hugging Face)

Install dependencies:

pip install datasets huggingface_hub


Fetch and prepare data:

datasetqa-fetch-bones --source mura --out-dir ./examples/bones_real --max 60


Review and export:

python -m datasetqa.review --image-dir ./examples/bones_real/broken_bone --type BB --overwrite
python -m datasetqa.review --image-dir ./examples/bones_real/non_broken --type NB --overwrite
datasetqa-export --image-dir ./examples/bones_real/broken_bone --type BB --out bones_real_bb.csv
datasetqa-export --image-dir ./examples/bones_real/non_broken --type NB --out bones_real_nb.csv

Docker Quickstart

Build and run inside a container:

docker build -t datasetqa:latest .
docker run --rm -it -p 8888:8888 -v "$PWD":/app datasetqa:latest bash


Inside the container:

datasetqa-fetch-bones --source mura --out-dir ./examples/bones_real --max 60
python -m datasetqa.review --image-dir ./examples/bones_real/broken_bone --type BB
datasetqa-export --image-dir ./examples/bones_real/broken_bone --type BB --out bones_real_bb.csv

Jupyter Notebook Demo

The notebook notebooks/bones_baseline.ipynb demonstrates:

Loading and preprocessing labeled X-ray data

Training a baseline logistic regression model

Plotting a confusion matrix and predictions

Run in VS Code

Open the notebook

Select your .venv Python 3.11 kernel

Choose Run All

License

MIT License © 2025 Ryan Furman
Free for research and educational use.
