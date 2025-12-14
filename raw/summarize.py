#!/usr/bin/env python3
import os
import json
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

# Load the chapters from the JSON file
with open("chapters.json", "r", encoding="utf-8") as f:
    chapters = json.load(f)

# Iterate over all entries
for chapter in chapters:
    title = chapter["title"]
    content = chapter["content"]
    print(f"\nChapter: {title}")
    # Print first 100 characters of content as preview
    #print(f"Preview: {content[:100]}...")
    prompt = f'I besitze das Buch "PHILOSOPHIE DES ABENDLANDES". Es folgt das Kapitel "{title}". Bitte fass das Kapitel KNAPP auf Deutsch zusammen. Fokussiere dich auf die beschriebenen Konzepte. Verwende reinen Text, keine Formatierung, kein Markdown. GENAU 1 Absatz, MAXIMAL 5 Sätze, MAXIMAL 50 Wörtern insgesamt. Ich kenne bereits den Titel des Kapitels. Fokussiere dich auf die philosophischen Konzepte. Ich werde dich später befragen, dabei darfst du das Kapitel nochmal lesen, musst es aber anhand deiner Zusammenfassung wiederfinden. Der Inhalt:\n\n' + content
    chat_response = client.chat.complete(
        model = model,
        messages = [
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )
    print(chat_response.usage)
    print(f"len(chat_response.choices): {len(chat_response.choices)}")
    print(f"chat_response.choices[0].finish_reason: {chat_response.choices[0].finish_reason}")
    print()

    summary = chat_response.choices[0].message.content

    print('Summary:\n', '>>>' + summary + '<<<')
    chapter["summary"] = summary


with open("chapters_with_summaries.json", "w", encoding="utf-8") as f:
    json.dump(chapters, f, ensure_ascii=False, indent=4)

