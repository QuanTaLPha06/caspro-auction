#!/usr/bin/env python3
"""
Free, offline background remover.

Uses rembg (U^2-Net / BiRefNet) which runs entirely on your machine.
No API keys, no uploads, no cost.

Setup (one time):
    pip install "rembg[cpu]" pillow
    # or for GPU (much faster if you have an NVIDIA card + CUDA):
    # pip install "rembg[gpu]" pillow

Usage:
    python remove_bg.py input.jpg
    python remove_bg.py input.jpg -o output.png
    python remove_bg.py ./photos                 # whole folder
    python remove_bg.py input.jpg --model isnet-general-use
    python remove_bg.py input.jpg --alpha-matting  # cleaner edges (slower)
"""

import argparse
import sys
from pathlib import Path

try:
    from rembg import new_session, remove
    from PIL import Image
except ImportError:
    sys.exit(
        "Missing dependencies. Install with:\n"
        '    pip install "rembg[cpu]" pillow'
    )

# Formats we'll process when given a folder
SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


def process_one(src: Path, dst: Path, session, alpha_matting: bool) -> None:
    """Remove background from a single image, writing a lossless PNG."""
    # Load original at full resolution; convert to RGBA so alpha survives.
    img = Image.open(src).convert("RGBA")

    result = remove(
        img,
        session=session,
        alpha_matting=alpha_matting,
        # These only matter when alpha_matting=True; sane defaults:
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10,
    )

    # PNG is lossless and keeps the alpha (transparency) channel intact.
    # compress_level=6 is zlib compression — lossless, just smaller files.
    result.save(dst, format="PNG", compress_level=6)
    print(f"  {src.name} -> {dst.name}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove image backgrounds for free, fully offline."
    )
    parser.add_argument("input", help="Image file or a folder of images")
    parser.add_argument(
        "-o", "--output",
        help="Output file (single input) or folder. Default: alongside input.",
    )
    parser.add_argument(
        "--model",
        default="u2net",
        help=(
            "Segmentation model. Good options:\n"
            "  birefnet-general  (best quality, larger download)\n"
            "  isnet-general-use (great all-rounder)\n"
            "  u2net             (classic default)\n"
            "  u2net_human_seg   (people/portraits)"
        ),
    )
    parser.add_argument(
        "--alpha-matting",
        action="store_true",
        help="Refine edges (hair, fur). Slower but cleaner.",
    )
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        sys.exit(f"Input not found: {in_path}")

    # Build the model session once and reuse it (downloads model on first run).
    print(f"Loading model '{args.model}' (first run downloads it once)...")
    session = new_session(args.model)

    # Gather the list of (source, destination) pairs.
    jobs = []
    if in_path.is_dir():
        out_dir = Path(args.output) if args.output else in_path / "no_bg"
        out_dir.mkdir(parents=True, exist_ok=True)
        for f in sorted(in_path.iterdir()):
            if f.suffix.lower() in SUPPORTED:
                jobs.append((f, out_dir / f"{f.stem}.png"))
        if not jobs:
            sys.exit(f"No supported images found in {in_path}")
    else:
        if args.output:
            dst = Path(args.output)
            if dst.suffix.lower() != ".png":
                dst = dst.with_suffix(".png")  # force lossless PNG
        else:
            dst = in_path.with_name(f"{in_path.stem}_no_bg.png")
        jobs.append((in_path, dst))

    print(f"Processing {len(jobs)} image(s):")
    for src, dst in jobs:
        try:
            process_one(src, dst, session, args.alpha_matting)
        except Exception as e:  # keep going on batch runs
            print(f"  ! Failed on {src.name}: {e}")

    print("Done.")


if __name__ == "__main__":
    main()
