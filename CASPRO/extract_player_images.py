#!/usr/bin/env python3
"""
extract_player_images.py

Extracts player photographs from the IPL Auction Deck PDF and saves each
one labeled by player number and player name, e.g.:

    001_Virat_Kohli.png
    002_Rohit_Sharma.png
    ...
"""

import csv
import os
import re
import sys

# Try importing fitz (PyMuPDF); if not available, fallback to pypdf
try:
    import fitz  # PyMuPDF
    USE_FITZ = True
except ImportError:
    import pypdf
    USE_FITZ = False

PLAYER_LINE_RE = re.compile(r"#\s*(\d+)\s*-\s*(.+)")
SMALL_PHOTO_WARNING_AREA = 40_000
MIN_PHOTO_AREA = 5_000


def sanitize_filename(name: str) -> str:
    """Turn a player name into a filesystem-safe filename fragment."""
    name = name.strip()
    name = re.sub(r"[^\w\s\-']", "", name)
    name = re.sub(r"\s+", "_", name)
    return name.strip("_") or "Unknown"


def find_player_info(page_text: str):
    """Return (player_number, player_name) for the first match on the page, or None."""
    for line in page_text.splitlines():
        match = PLAYER_LINE_RE.search(line)
        if match:
            number = match.group(1).strip()
            name = match.group(2).strip()
            name = name.split("\n")[0].strip()
            return number, name
    return None


def extract_player_images_fitz(pdf_path: str, output_dir: str):
    doc = fitz.open(pdf_path)
    log_rows = []
    saved_count = 0

    for page_index in range(len(doc)):
        page = doc[page_index]
        page_number = page_index + 1
        page_text = page.get_text()

        info = find_player_info(page_text)
        if info is None:
            log_rows.append({
                "page": page_number,
                "player_number": "",
                "player_name": "",
                "status": "skipped_no_player_text",
                "saved_file": "",
            })
            continue

        player_number, player_name = info
        image_list = page.get_images(full=True)

        if not image_list:
            log_rows.append({
                "page": page_number,
                "player_number": player_number,
                "player_name": player_name,
                "status": "no_images_found",
                "saved_file": "",
            })
            continue

        best_xref = None
        best_area = 0

        for img in image_list:
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
            except Exception:
                continue
            width = base_image.get("width", 0)
            height = base_image.get("height", 0)
            area = width * height
            if area > best_area:
                best_area = area
                best_xref = xref

        if best_xref is None or best_area < MIN_PHOTO_AREA:
            log_rows.append({
                "page": page_number,
                "player_number": player_number,
                "player_name": player_name,
                "status": f"photo_too_small_or_missing (best_area={best_area})",
                "saved_file": "",
            })
            continue

        base_image = doc.extract_image(best_xref)
        image_bytes = base_image["image"]
        ext = base_image.get("ext", "png")

        safe_name = sanitize_filename(player_name)
        padded_number = player_number.zfill(3)
        filename = f"{padded_number}_{safe_name}.{ext}"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        saved_count += 1
        status = "saved" if best_area >= SMALL_PHOTO_WARNING_AREA else f"saved_but_small (area={best_area})"
        log_rows.append({
            "page": page_number,
            "player_number": player_number,
            "player_name": player_name,
            "status": status,
            "saved_file": filename,
        })
        print(f"[page {page_number}] Saved: {filename}")

    doc.close()
    return saved_count, log_rows


def extract_player_images_pypdf(pdf_path: str, output_dir: str):
    reader = pypdf.PdfReader(pdf_path)
    log_rows = []
    saved_count = 0

    for page_index, page in enumerate(reader.pages):
        page_number = page_index + 1
        page_text = page.extract_text() or ""

        info = find_player_info(page_text)
        if info is None:
            log_rows.append({
                "page": page_number,
                "player_number": "",
                "player_name": "",
                "status": "skipped_no_player_text",
                "saved_file": "",
            })
            continue

        player_number, player_name = info

        images = []
        try:
            for img in page.images:
                data = img.data
                ext = os.path.splitext(img.name)[1].lstrip(".").lower() or "jpg"
                images.append({
                    "data": data,
                    "ext": ext,
                    "size": len(data),
                    "name": img.name,
                })
        except Exception as e:
            print(f"[page {page_number}] Warning reading images: {e}")

        if not images:
            log_rows.append({
                "page": page_number,
                "player_number": player_number,
                "player_name": player_name,
                "status": "no_images_found",
                "saved_file": "",
            })
            continue

        # Pick the largest image by byte size
        best_img = max(images, key=lambda x: x["size"])

        if best_img["size"] < 3000:
            log_rows.append({
                "page": page_number,
                "player_number": player_number,
                "player_name": player_name,
                "status": f"photo_too_small_or_missing (size={best_img['size']})",
                "saved_file": "",
            })
            continue

        safe_name = sanitize_filename(player_name)
        padded_number = player_number.zfill(3)
        filename = f"{padded_number}_{safe_name}.{best_img['ext']}"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "wb") as f:
            f.write(best_img["data"])

        saved_count += 1
        log_rows.append({
            "page": page_number,
            "player_number": player_number,
            "player_name": player_name,
            "status": "saved",
            "saved_file": filename,
        })
        print(f"[page {page_number}] Saved: {filename}")

    return saved_count, log_rows


def extract_player_images(pdf_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    if USE_FITZ:
        print("Using PyMuPDF (fitz) backend...")
        saved_count, log_rows = extract_player_images_fitz(pdf_path, output_dir)
    else:
        print("Using pypdf backend...")
        saved_count, log_rows = extract_player_images_pypdf(pdf_path, output_dir)

    log_path = os.path.join(output_dir, "extraction_log.csv")
    with open(log_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["page", "player_number", "player_name", "status", "saved_file"]
        )
        writer.writeheader()
        writer.writerows(log_rows)

    # Generate manifest for frontend
    import json
    manifest = {}
    if os.path.exists(output_dir):
        for fname in os.listdir(output_dir):
            match = re.match(r"^(\d+)_", fname)
            if match:
                pid = int(match.group(1))
                manifest[pid] = f"/player_images/{fname}"
    manifest_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "player_images_manifest.json")
    try:
        with open(manifest_path, "w", encoding="utf-8") as mf:
            json.dump(manifest, mf, indent=2)
        print(f"Manifest written to '{manifest_path}'.")
    except Exception as e:
        print(f"Warning: Could not write manifest: {e}")

    print(f"\nDone. {saved_count} player images saved to '{output_dir}'.")
    print(f"Full log written to '{log_path}'.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract_player_images.py <input.pdf> [output_dir]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "player_images"

    if not os.path.exists(pdf_path):
        print(f"Error: file not found: {pdf_path}")
        sys.exit(1)

    extract_player_images(pdf_path, output_dir)


if __name__ == "__main__":
    main()

