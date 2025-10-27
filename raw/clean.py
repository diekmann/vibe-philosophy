#!/usr/bin/env python3
import re

def remove_footnotes_by_paragraph(text: str) -> str:
    # Split into paragraphs separated by one or more blank lines
    paragraphs = re.split(r'\n\s*\n', text)
    kept = []
    for p in paragraphs:
        stripped = p.lstrip()
        # Remove paragraph if it starts with "* " or "** "
        if stripped.startswith('* ') or stripped.startswith('** '):
            continue
        kept.append(p)
    # Rejoin with a single blank line between paragraphs
    return '\n\n'.join(kept)

# Input and output file paths
input_file = "PHILOSOPHIE_DES_ABENDLANDES_VON_BERTRAND_RUSSEL_djvu.txt"
output_file = "PHILOSOPHIE_DES_ABENDLANDES_CLEANED.txt"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

text = remove_footnotes_by_paragraph(text)

# Remove page numbers and headers
text = re.sub(r'\n\n\d+\s*\n\n[A-ZÄÖÜß\s]+\n\n', '\n', text)
text = re.sub(r'\n\n[A-ZÄÖÜß\s]+\n\n\d+\s*\n\n', '\n', text)

# Clean up multiple blank lines ---
text = re.sub(r'\n{3,}', '\n\n', text)

text = re.split(r'\nREGISTER, \n', text, maxsplit=1, flags=re.MULTILINE)[0]

# Write the cleaned text
with open(output_file, "w", encoding="utf-8") as f:
    f.write(text)

print("Cleaning complete. Saved to:", output_file)
