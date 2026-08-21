#!/usr/bin/env python3
"""
IPL Auction Player Photo Downloader
------------------------------------
Pulls each player's main portrait photo from Wikipedia (sourced from
Wikimedia Commons), reading directly from players.json.

For every player it saves:
  images/<id:03d>_<slug>.jpg       - the photo
  credits.json                     - license + attribution info per player
  missing.csv                      - players with no usable Wikipedia image

Usage:
    pip install requests
    python3 download_images.py
"""

import json
import os
import re
import time
import csv
import requests

OUT_DIR = "images"
API = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "IPLAuctionPhotoFetcher/1.0 (personal fan project; contact: none)"}

os.makedirs(OUT_DIR, exist_ok=True)


def slugify(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", name).strip("_").lower()
    return s


def find_wikipedia_page(name: str):
    """Search Wikipedia for the best-matching page, biased toward cricket."""
    params = {
        "action": "query",
        "list": "search",
        "srsearch": f"{name} cricketer",
        "format": "json",
        "srlimit": 3,
    }
    r = requests.get(API, params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    results = r.json().get("query", {}).get("search", [])
    if not results:
        # fallback: plain name search
        params["srsearch"] = name
        r = requests.get(API, params=params, headers=HEADERS, timeout=15)
        r.raise_for_status()
        results = r.json().get("query", {}).get("search", [])
    if not results:
        return None
    return results[0]["title"]


def get_page_image_info(title: str):
    """Get the main infobox image (pageimage) + its Commons metadata."""
    params = {
        "action": "query",
        "titles": title,
        "prop": "pageimages|imageinfo",
        "piprop": "original",
        "iiprop": "extmetadata|url",
        "format": "json",
    }
    r = requests.get(API, params=params, headers=HEADERS, timeout=15)
    r.raise_for_status()
    pages = r.json().get("query", {}).get("pages", {})
    page = next(iter(pages.values()), None)
    if not page:
        return None

    original = page.get("original", {}).get("source")
    if not original:
        return None

    # Fetch license metadata directly from the file page for accurate credit
    fname = original.split("/")[-1]
    file_title = f"File:{requests.utils.unquote(fname)}"

    meta_params = {
        "action": "query",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "extmetadata|url",
        "format": "json",
    }
    mr = requests.get(API, params=meta_params, headers=HEADERS, timeout=15)
    mr.raise_for_status()
    mpages = mr.json().get("query", {}).get("pages", {})
    mpage = next(iter(mpages.values()), {})
    imageinfo = (mpage.get("imageinfo") or [{}])[0]
    extmeta = imageinfo.get("extmetadata", {})

    def meta(key):
        return extmeta.get(key, {}).get("value", "")

    license_short = re.sub("<[^<]+?>", "", meta("LicenseShortName")) or "See file page"
    artist = re.sub("<[^<]+?>", "", meta("Artist")) or "Unknown"
    credit = re.sub("<[^<]+?>", "", meta("Credit")) or ""

    return {
        "image_url": original,
        "wikipedia_page": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
        "file_page": imageinfo.get("descriptionurl", ""),
        "license": license_short,
        "artist": artist,
        "credit_line": credit,
    }


def download_image(url: str, dest_path: str) -> bool:
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(r.content)
        return True
    except Exception as e:
        print(f"    download failed: {e}")
        return False


def main():
    if not os.path.exists("players.json"):
        print("Error: players.json not found!")
        return

    with open("players.json", "r", encoding="utf-8") as f:
        players_data = json.load(f)

    credits = {}
    missing = []

    print(f"Loaded {len(players_data)} players from players.json. Starting download...\n")

    for p in players_data:
        lot = p.get("id")
        name = p.get("name")
        pool = p.get("pool", p.get("pool_name", ""))
        slug = slugify(name)

        print(f"[{lot:03d}] {name} (Pool {pool}) ...")

        try:
            title = find_wikipedia_page(name)
            if not title:
                print("    no Wikipedia page found")
                missing.append((lot, name, pool, "no wikipedia page"))
                continue

            info = get_page_image_info(title)
            if not info:
                print("    no image on page")
                missing.append((lot, name, pool, "no image on page"))
                continue

            # Parse extension properly from URL path
            raw_path = info["image_url"].split("?")[0]
            ext = os.path.splitext(raw_path)[1].lstrip(".").lower() or "jpg"
            if len(ext) > 4:
                ext = "jpg"
            fname = f"{lot:03d}_{slug}.{ext}"
            dest = os.path.join(OUT_DIR, fname)

            ok = download_image(info["image_url"], dest)
            if not ok:
                missing.append((lot, name, pool, "download failed"))
                continue

            credits[fname] = {
                "lot": lot,
                "player": name,
                "pool": pool,
                "source": "Wikipedia / Wikimedia Commons",
                "wikipedia_page": info["wikipedia_page"],
                "file_page": info["file_page"],
                "license": info["license"],
                "artist": info["artist"],
                "credit_line": info["credit_line"],
                "attribution": f'Photo: {info["artist"]} via Wikimedia Commons, {info["license"]}',
            }
            print(f"    saved -> {fname}  [{info['license']}]")

        except requests.exceptions.RequestException as e:
            print(f"    network error: {e}")
            missing.append((lot, name, pool, f"error: {e}"))

        time.sleep(0.3)  # be polite to Wikipedia API

    with open("credits.json", "w", encoding="utf-8") as f:
        json.dump(credits, f, indent=2, ensure_ascii=False)

    with open("missing.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["lot", "name", "pool", "reason"])
        writer.writerows(missing)

    print(f"\nDone. {len(credits)} images saved, {len(missing)} missing.")
    print("See credits.json for attribution.")
    print("See missing.csv for players without Wikipedia images.")


if __name__ == "__main__":
    main()
