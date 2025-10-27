#!/usr/bin/env python3
import re
import json

input_file = "PHILOSOPHIE_DES_ABENDLANDES_CLEANED.txt"


def split_into_chapters(text):
    # Pattern to match chapters like "24. Kapitel" optionally followed by a title
    pattern = re.compile(r'(\d+\.\s*Kapitel\.? *\n *\n?(?:[A-ZÄÖÜ][A-ZÄÖÜa-zäöüß -]*)?)', re.MULTILINE)

    # Split text by the pattern but keep the delimiters
    parts = pattern.split(text)

    chapters = list()
    current_title = None

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # If this part is a chapter title
        if re.match(pattern, part):
            # Normalize title with colon between number and name if missing
            if ':' not in part and 'Kapitel' in part:
                part = part.replace('Kapitel', 'Kapitel:').replace('::', ':')
            current_title = part.replace('\n', ' ').strip()
        elif current_title:
            # Append text content to current chapter
            entry = (current_title, part.strip() + '\n')
            chapters.append(entry)

    return chapters

# Read the text
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

chapters = split_into_chapters(text)


## Display results (optional)
#for title, content in chapters:
#    #print(f"{title}:\n{'-'*len(title)}\n{content}\n")
#    print(f">>>{title}<<<")
#    print(content)
#    print("\n\n")


# Write chapters to JSON file
output_file = "chapters.json"
with open(output_file, "w", encoding="utf-8") as jf:
    json.dump([{"title": t, "content": c} for t, c in chapters], jf, ensure_ascii=False, indent=2)