"""Generate sample images for recognition demos."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SAMPLES_DIR = Path(__file__).resolve().parent


def create_text_sample() -> Path:
    """Image with printed text for OCR demo."""
    path = SAMPLES_DIR / "sample_text.png"
    img = Image.new("RGB", (400, 120), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except OSError:
        font = ImageFont.load_default()
    draw.text((20, 40), "Decode Labs 2026", fill=(0, 0, 0), font=font)
    img.save(path)
    return path


def create_object_sample() -> Path:
    """Simple colored shapes as a stand-in when no photo is available."""
    path = SAMPLES_DIR / "sample_object.png"
    img = Image.new("RGB", (224, 224), color=(70, 130, 180))
    draw = ImageDraw.Draw(img)
    draw.ellipse([40, 40, 180, 180], fill=(255, 200, 50), outline=(200, 120, 0), width=4)
    draw.rectangle([120, 120, 200, 200], fill=(50, 180, 80))
    img.save(path)
    return path


if __name__ == "__main__":
    create_text_sample()
    create_object_sample()
    print(f"Samples saved in {SAMPLES_DIR}")
