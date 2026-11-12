"""Measure the input quality of the sampled wellbore diagram PDFs.

Usage (from this folder):
    python profile_pdf_quality.py

Reads sample/diagrams/W01.pdf ... W30.pdf (read only; the files are not changed)
and writes sample/pdf-quality-profile.csv. Definitions are in
sample/sample-quality-evaluation.txt, section 3.

Requires PyMuPDF (pip install pymupdf).
"""
import csv
import statistics
from pathlib import Path

import pymupdf

HERE = Path(__file__).parent
DIAGRAMS = HERE / "sample" / "diagrams"
OUT = HERE / "sample" / "pdf-quality-profile.csv"

# Observations made by looking at each page; not measurable from the file.
VISUAL_NOTES = {
    "W11": "Page content is printed sideways (landscape layout); readable after rotating.",
    "W15": "Two pages covering three boreholes (two abandoned, one current).",
    "W17": "Template title reads 'Proposed Diagram'; sheet stamped CURRENT.",
}


def classify(text_chars, raster_coverage):
    if text_chars < 50:
        return "Scanned"
    if text_chars < 1000 and raster_coverage >= 0.25:
        return "Mixed"
    return "Native"


def profile(path):
    doc = pymupdf.open(path)
    first = doc[0]
    page_area = first.rect.width * first.rect.height
    chars = words = images = 0
    fonts, largest = [], None          # largest = (area, dpi) of the biggest raster image
    for page in doc:
        chars += len(page.get_text().strip())
        words += len(page.get_text("words"))
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    if span["text"].strip():
                        fonts.append(span["size"])
        for info in page.get_image_info():
            images += 1
            x0, y0, x1, y1 = info["bbox"]
            area = max(0.0, (x1 - x0) * (y1 - y0))
            if (x1 - x0) > 0 and info.get("width"):
                dpi = info["width"] / ((x1 - x0) / 72)
                if largest is None or area > largest[0]:
                    largest = (area, dpi)
    coverage = min(1.0, largest[0] / page_area) if largest else 0.0
    w_in, h_in = first.rect.width / 72, first.rect.height / 72
    return {
        "SampleCode": path.stem,
        "Pages": doc.page_count,
        "FileKB": round(path.stat().st_size / 1024),
        "PageWidthIn": round(w_in, 1),
        "PageHeightIn": round(h_in, 1),
        "Orientation": "Landscape" if w_in > h_in else "Portrait",
        "TextChars": chars,
        "Words": words,
        "RasterImages": images,
        "LargestImagePageCoverage": round(coverage, 2),
        "LargestImageDPI": round(largest[1]) if largest else "",
        "MinFontPt": round(min(fonts), 1) if fonts else "",
        "MedianFontPt": round(statistics.median(fonts), 1) if fonts else "",
        "InputType": classify(chars, coverage),
        "VisualNotes": VISUAL_NOTES.get(path.stem, ""),
    }


def main():
    rows = [profile(p) for p in sorted(DIAGRAMS.glob("W*.pdf"))]
    with open(OUT, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    for kind in ("Native", "Mixed", "Scanned"):
        codes = [r["SampleCode"] for r in rows if r["InputType"] == kind]
        print(f"{kind:8} {len(codes):2}  {' '.join(codes)}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
