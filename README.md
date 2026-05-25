# Project 4: Image or Text Recognition (Basic)

Decode Labs assignment — classify images with a pretrained ResNet18 and read text from images with EasyOCR. No model training.

**Full write-up:** [DOCUMENTATION.docx](DOCUMENTATION.docx) (Word) · [DOCUMENTATION.md](DOCUMENTATION.md) (markdown)

## Quick start

```powershell
cd "Project_4_Image or Text Recogination(basic)"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python recognize.py
```

First run downloads model weights and creates sample images in `samples/`.

## Commands

```powershell
python recognize.py                    # both modes
python recognize.py --mode image       # classification only
python recognize.py --mode text        # OCR only
python recognize.py --image photo.jpg --text-image scan.png
```

## Files

- `recognize.py` — main script
- `samples/` — demo images (auto-created)
- `DOCUMENTATION.md` — project documentation
