"""
Project 4: Image or Text Recognition (Basic)

Uses pre-trained libraries only:
  - torchvision ResNet18 for image classification
  - EasyOCR for text extraction from images
"""

from __future__ import annotations

import argparse
from pathlib import Path

import easyocr
import torch
from PIL import Image
from torchvision import models, transforms
from torchvision.models import ResNet18_Weights

ROOT = Path(__file__).resolve().parent
SAMPLES = ROOT / "samples"


def ensure_samples() -> None:
    """Create sample images if they do not exist."""
    if (SAMPLES / "sample_text.png").exists() and (SAMPLES / "sample_object.png").exists():
        return
    from samples.create_samples import create_object_sample, create_text_sample

    create_text_sample()
    create_object_sample()


def load_image_classifier():
    weights = ResNet18_Weights.DEFAULT
    model = models.resnet18(weights=weights)
    model.eval()
    preprocess = weights.transforms()
    categories = weights.meta["categories"]
    return model, preprocess, categories


def recognize_image(image_path: Path) -> None:
    """Classify image content using a pre-trained ResNet18 model."""
    print("\n" + "=" * 60)
    print("IMAGE RECOGNITION (Pre-trained ResNet18)")
    print("=" * 60)
    print(f"Input: {image_path.resolve()}")

    model, preprocess, categories = load_image_classifier()
    image = Image.open(image_path).convert("RGB")
    batch = preprocess(image).unsqueeze(0)

    with torch.no_grad():
        logits = model(batch)
        probabilities = torch.nn.functional.softmax(logits[0], dim=0)

    top5_prob, top5_idx = torch.topk(probabilities, 5)

    print("\nTop 5 predictions:")
    print("-" * 60)
    for rank, (prob, idx) in enumerate(zip(top5_prob, top5_idx), start=1):
        label = categories[idx]
        print(f"  {rank}. {label:<30} {prob.item() * 100:5.2f}%")
    print("-" * 60)
    best_label = categories[top5_idx[0]]
    print(f"\nResult: This image is most likely \"{best_label}\"")
    print(f"        (confidence: {top5_prob[0].item() * 100:.2f}%)")


def recognize_text(image_path: Path) -> None:
    """Extract text from an image using EasyOCR."""
    print("\n" + "=" * 60)
    print("TEXT RECOGNITION / OCR (EasyOCR)")
    print("=" * 60)
    print(f"Input: {image_path.resolve()}")

    reader = easyocr.Reader(["en"], gpu=torch.cuda.is_available(), verbose=False)
    results = reader.readtext(str(image_path))

    if not results:
        print("\nNo text detected in the image.")
        return

    print("\nDetected text regions:")
    print("-" * 60)
    for i, (bbox, text, confidence) in enumerate(results, start=1):
        print(f"  {i}. Text: \"{text}\"")
        print(f"     Confidence: {confidence * 100:.2f}%")
        print(f"     Bounding box: {bbox}")
    print("-" * 60)

    full_text = " ".join(item[1] for item in results)
    avg_conf = sum(item[2] for item in results) / len(results)
    print(f"\nResult: \"{full_text.strip()}\"")
    print(f"        (average confidence: {avg_conf * 100:.2f}%)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Basic image or text recognition using pre-trained libraries."
    )
    parser.add_argument(
        "--mode",
        choices=["image", "text", "both"],
        default="both",
        help="Recognition mode: image classification, OCR, or both (default: both)",
    )
    parser.add_argument(
        "--image",
        type=Path,
        default=None,
        help="Path to image for classification (default: samples/sample_object.png)",
    )
    parser.add_argument(
        "--text-image",
        type=Path,
        default=None,
        help="Path to image for OCR (default: samples/sample_text.png)",
    )
    args = parser.parse_args()

    ensure_samples()

    image_path = args.image or (SAMPLES / "sample_object.png")
    text_image_path = args.text_image or (SAMPLES / "sample_text.png")

    if args.mode in ("image", "both"):
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        recognize_image(image_path)

    if args.mode in ("text", "both"):
        if not text_image_path.exists():
            raise FileNotFoundError(f"Text image not found: {text_image_path}")
        recognize_text(text_image_path)

    print("\nDone.\n")


if __name__ == "__main__":
    main()
