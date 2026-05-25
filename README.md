# Project 4: Image or Text Recognition (Basic)

A small Python project for **Decode Labs** that runs two kinds of recognition on images—no training, no custom models. Everything uses off-the-shelf libraries and pretrained weights.

- **Image recognition** — guess what’s in a photo (ImageNet labels via ResNet18)
- **Text recognition** — read words from an image (OCR via EasyOCR)

---

## Overview

The goal of the assignment is to use existing AI libraries, feed them sample input, and show the results in a clear way. This repo does that through a single CLI script: `recognize.py`.

On the first run, the script creates two demo images under `samples/` so you can test without hunting for files. You can swap in your own photos anytime.

For a longer explanation (setup notes, how to read the output, assignment checklist), see:

- **[DOCUMENTATION.docx](DOCUMENTATION.docx)** — formatted for Word / submission    

---

## Features

| Feature | Library | What you get |
|---------|---------|--------------|
| Object classification | `torchvision` (ResNet18) | Top 5 labels with confidence % |
| Text extraction (OCR) | `easyocr` | Detected text, per-line confidence, bounding boxes |
| Sample images | `Pillow` | Auto-generated PNGs if `samples/` is empty |
| Modes | CLI flags | Run image only, text only, or both |

---

## Requirements

- **Python** 3.11+ (3.12 or 3.14 also work; use a virtual environment)
- **Windows** — instructions below use PowerShell; the script runs on macOS/Linux with the usual `python3` / `source venv/bin/activate` changes
- **Disk space** — PyTorch and EasyOCR are large; first run also downloads model weights (~150MB+ total)
- **Internet** — needed on first run to download ResNet and EasyOCR models

---

## Installation

Clone or open the project folder, then:

```powershell
cd "C:\path\to\Project_4_Image or Text Recogination(basic)"

python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

`pip install` may take several minutes because of PyTorch.

---

## Usage

Activate the virtual environment, then run from the project root:

```powershell
.\venv\Scripts\activate

# Default: run image classification + OCR on built-in samples
python recognize.py

# Classification only
python recognize.py --mode image

# OCR only
python recognize.py --mode text

# Your own files
python recognize.py --image "C:\photos\dog.jpg" --text-image "C:\photos\receipt.png"
```

### CLI options

| Option | Default | Description |
|--------|---------|-------------|
| `--mode` | `both` | `image`, `text`, or `both` |
| `--image` | `samples/sample_object.png` | Image for ResNet18 classification |
| `--text-image` | `samples/sample_text.png` | Image for EasyOCR |

### Regenerate sample images

```powershell
python samples/create_samples.py
```

---

## Example output

**Image mode** — top predictions with softmax percentages:

```
Top 5 predictions:
------------------------------------------------------------
  1. golden retriever               42.31%
  2. Labrador retriever            18.02%
  ...
Result: This image is most likely "golden retriever"
        (confidence: 42.31%)
```

**Text mode** — OCR on the sample that says “Decode Labs 2026”:

```
  1. Text: "Decode Labs 2026"
     Confidence: 99.65%
Result: "Decode Labs 2026"
```

> The bundled `sample_object.png` is a simple drawn shape, not a real photo. ResNet was trained on real images, so confidence on that file will look low. Use a normal JPG for a fair test.

---

## Project structure

```
Project_4_Image or Text Recogination(basic)/
├── recognize.py              # Main entry point
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── DOCUMENTATION.docx        # Word version of documentation
├── samples/
│   ├── create_samples.py     # Creates demo PNGs
│   ├── sample_object.png     # Created on first run
│   └── sample_text.png       # Created on first run
└── venv/                     # Local environment (gitignored)
```

---

## How it works (short version)

1. **`recognize_image`** loads pretrained ResNet18, preprocesses the image with torchvision’s default transforms, runs inference, and prints the top 5 ImageNet classes.
2. **`recognize_text`** initializes EasyOCR for English, runs `readtext()` on the image path, and prints each detected string with confidence and box coordinates.
3. **`ensure_samples`** checks for demo files and creates them via `samples/create_samples.py` if missing.

Inference only—`model.eval()` and `torch.no_grad()`; no training loop.

---

## Dependencies

Listed in `requirements.txt`:

```
torch
torchvision
Pillow
easyocr
```

EasyOCR installs additional packages (OpenCV headless, scipy, etc.) automatically.

---

## Troubleshooting

| Issue | What to try |
|-------|-------------|
| First run very slow | Normal—models download once. Wait for ResNet / EasyOCR to finish. |
| `&&` not recognized in PowerShell | Run commands separately, or use `;` between them. |
| Low classification confidence | Use a real photo instead of `sample_object.png`. |
| `No text detected` | Use a clearer image; check contrast and font size. |
| `ModuleNotFoundError` | Activate `venv` and run `pip install -r requirements.txt` again. |
| CUDA / pin_memory warning | Safe to ignore on CPU-only machines. |

---

## Assignment mapping

| Requirement | Implementation |
|-------------|----------------|
| Pre-trained model or library | ResNet18 (torchvision), EasyOCR |
| Sample input | Auto-generated `samples/*.png` + custom paths |
| Clear output | Formatted console sections with labels and confidence |
| AI libraries | `torch`, `torchvision`, `easyocr` |
| Understanding outputs | Softmax probabilities; OCR confidence and bounding boxes |

---

## Documentation

| File | Purpose |
|------|---------|
| `README.md` | Quick reference (this file) |
| `DOCUMENTATION.docx` | Same guide for Word / PDF export |

To rebuild the Word doc after editing the export script:

```powershell
.\venv\Scripts\python export_documentation.py
```

---

## License & context

Built as part of **Decode Labs — Project 4: Image or Text Recognition (Basic)**.

Personal / educational use. Third-party models (PyTorch ImageNet weights, EasyOCR) are subject to their own licenses.
