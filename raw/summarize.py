#! /usr/bin/env python3
import json
from ollama import Client

client = Client(
    host="http://192.168.0.42:11434",
)

# Load the chapters from the JSON file
with open("chapters.json", "r", encoding="utf-8") as f:
    chapters = json.load(f)

# Iterate over all entries
for chapter in chapters:
    title = chapter["title"]
    content = chapter["content"]
    print(f"\nChapter: {title}")
    # Print first 100 characters of content as preview
    print(f"Preview: {content[:100]}...")
    prompt = f'I besitze das Buch "PHILOSOPHIE DES ABENDLANDES". Es folgt das Kapitel "{title}". Bitte fass das Kapitel KNAPP zusammen. GENAU 1 Absatz, MAXIMAL 3 Sätze, MAXIMAL 30 Wörtern zusammen. Ich kenne bereits den Titel des Kapitels. Fokussiere dich auf die philosophischen Konzepte. Ich werde dich später befragen, dabei darfst du das Kapitel nochmal lesen, musst es aber anhand deiner Zusammenfassung wiederfinden. Der Inhalt:\n\n' + content
    # print(messages[0]['content'][:500] + '...')
    response = client.generate('gpt-oss:20b', prompt=prompt, think=True, options={'num_ctx': 65536})
    print('Summary:\n', '>>>' + response['response'] + '<<<')
    break
