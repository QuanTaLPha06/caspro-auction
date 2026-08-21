#!/usr/bin/env python3
"""
Extract player headshots from the IPL Auction Deck PDF using pypdf.

Each slide/page in the deck = one player, with photo(s) and a text
block starting with "#<lot> - <player name>".
"""

import os
import re
import sys
import csv
from pypdf import PdfReader

OUT_DIR = "images"


def slugify(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_").lower()


def parse_lot_and_name(page_text: str):
    if not page_text:
        return None, None
    lines = [line.strip() for line in page_text.strip().splitlines() if line.strip()]
    if not lines:
        return None, None
    
    first_line = lines[0]
    m = re.match(r"#\s*(\d+)\s*-\s*(.+)", first_line)
    if not m:
        # Check if first line is just #<lot> or similar
        m2 = re.search(r"#\s*(\d+)\s*-\s*(.+)", page_text)
        if not m2:
            return None, None
        m = m2

    lot = int(m.group(1))
    name_parts = [m.group(2).strip()]

    # Find where lines start after the initial header line match
    found_header = False
    for line in lines:
        if not found_header:
            if f"#{lot}" in line:
                found_header = True
            continue
        if line.startswith("Age:") or line.startswith("Role:") or line.startswith("Country:"):
            break
        name_parts.append(line)

    name = " ".join(p for p in name_parts if p)
    return lot, name


def extract_page_image_pypdf(page, dest_path: str) -> bool:
    try:
        images = list(page.images)
        if not images:
            return False
        
        # Pick the largest image by data size (headshot is larger than small logos)
        best_img = max(images, key=lambda img: len(img.data))
        ext = os.path.splitext(dest_path)[1]
        
        with open(dest_path, "wb") as f:
            f.write(best_img.data)
        return True
    except Exception as e:
        print(f"    pypdf extraction error: {e}")
        return False


def main():
    pdf_path = r"D:\Case\CASPRO\scripts\IPL_Auction_Deck_2026.pptx.pptx.pdf"
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)
    log_rows = []

    reader = PdfReader(pdf_path)
    total = len(reader.pages)
    print(f"Found {total} pages in '{pdf_path}'.\n")

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        lot, name = parse_lot_and_name(text)

        if lot is None or name is None:
            print(f"[page {i}] could not parse name/lot")
            log_rows.append((i, "", "", "PARSE_FAILED"))
            continue

        slug = slugify(name)
        fname = f"{lot:03d}_{slug}.jpg"
        dest = os.path.join(OUT_DIR, fname)

        ok = extract_page_image_pypdf(page, dest)

        if ok:
            print(f"[page {i}] #{lot} {name} -> {fname}")
            log_rows.append((lot, name, fname, "OK"))
        else:
            print(f"[page {i}] #{lot} {name} -> NO IMAGE FOUND")
            log_rows.append((lot, name, "", "NO_IMAGE"))

    with open("extraction_log.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lot", "name", "filename", "status"])
        w.writerows(log_rows)

    ok_count = sum(1 for r in log_rows if r[3] == "OK")
    print(f"\nDone. {ok_count}/{len(log_rows)} images extracted into '{OUT_DIR}/'.")
    print("See extraction_log.csv for full results / any failures.")


if __name__ == "__main__":
    main()
