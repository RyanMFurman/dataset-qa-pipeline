# ---------- Runtime base ----------
FROM python:3.11-slim

# System deps for opencv and plotting headless
RUN apt-get update && apt-get install -y --no-install-recommends         build-essential gcc         libglib2.0-0 libgl1         git curl     && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Copy project
COPY . /app

# Install package (editable not needed in container) + deps
RUN pip install --no-cache-dir -e .     && pip install --no-cache-dir          opencv-python matplotlib pillow          datasets huggingface_hub scikit-learn pandas          jupyter

# Fetch a small sample on build to prove data flow works (optional but helpful for demos)
# Comment out if you prefer to pull at runtime.
RUN datasetqa-fetch-bones --source mura --out-dir ./examples/bones_real --max 30 || true

# Default command prints help
CMD [ "bash", "-lc", "echo 'Container ready. Try: python -m datasetqa.review --image-dir ./examples/bones_real/broken_bone --type BB --overwrite'" ]