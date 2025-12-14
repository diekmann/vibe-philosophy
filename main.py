#! /usr/bin/env python3

import os
import json

from typing import List

from rich import print

from mistralai import Mistral, ToolCall
from mistralai.models.assistantmessage import AssistantMessage
from mistralai.models.function import Function
from mistralai.models.toolmessage import ToolMessage
from mistralai.models.usermessage import UserMessage
from mistralai.models.systemmessage import SystemMessage

book = None
with open("raw/chapters_with_summaries.json", "r", encoding="utf-8") as f:
    book = json.load(f)


def sorry_for_the_bad_book_data(txt):
    return txt.replace(" ", "")

def lookup_chapter(title: str) -> str:
    for chapter in book:
        if sorry_for_the_bad_book_data(chapter["title"]) == sorry_for_the_bad_book_data(title):
            return chapter["content"]
    return "Kapitel nicht gefunden."


index = []
for chapter in book:
    index.append(f"""Titel: "{chapter["title"]}"\n{chapter["summary"]}""")


names_to_functions = {
    "lookup_chapter": lookup_chapter,
}

tools = [
    {
        "type": "function",
        "function": Function(
            name="lookup_chapter",
            description="Abrufen eines Kapitels im Buch PHILOSOPHIE DES ABENDLANDES nach, anhand des Titels des Kapitels.",
            parameters={
                "type": "object",
                "required": ["title"],
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Der Titel des Kapitels. Es folgt eine Liste det Titel, sowie deren Zusammenfassungen:\n\n" + "\n\n".join(index),
                    }
                },
            },
        ),
    },
]


def call_tool(tool_calls: List[ToolCall]) -> ToolMessage:
    assert len(tool_calls) == 1  # only one tool call supported for now
    tool_call = tool_calls[0]
    function_name = tool_call.function.name
    function_params = json.loads(tool_call.function.arguments)

    print(
        f"calling function_name: {function_name}, with function_params: {function_params}")

    function_result = names_to_functions[function_name](**function_params)
    print("function_result: " +
          function_result[:20] + "..." + f"{len(function_result)} more chars" if len(function_result) > 20 else function_result)

    return ToolMessage(
        name=function_name,
        content=function_result,
        tool_call_id=tool_call.id,
    )


def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"

    client = Mistral(api_key=api_key)

    prompt = "Was sagt die Philosophie zum Thema Bohnen?"
    print(prompt)

    messages = [
        SystemMessage(
            content="Du bist ein hilfreicher Assistent, der Fragen zum Buch PHILOSOPHIE DES ABENDLANDES von Bertrand Russell beantwortet. " \
            "Du kannst dazu die Funktion 'lookup_chapter' verwenden, um relevante Kapitel im Buch abzurufen. " \
            "Lese alle entsprechenden Kapitel, bevor du antwortest! " \
            "WICHTIG: Rufe dazu stets die Kapitel via lookup_chapter ab, bevor du eine Antwort gibts! " \
            "Halte deine Antworten kurz und prägnant. " \
            "Sprich gehobenes und formales Deutsch, aber baue Street Slang ein, wie Digga!"
        ),
        UserMessage(
            content=prompt
        ),
    ]

    response = client.chat.complete(
        model=model, messages=messages, tools=tools, temperature=0,
    )

    print(response)

    # plz retry if it didn't make a tool call!
    assert response.choices[0].finish_reason == "tool_calls", "Must make a tool call!"

    messages.append(
        AssistantMessage(
            content=response.choices[0].message.content,
            tool_calls=response.choices[0].message.tool_calls,
        )
    )
    messages.append(
        call_tool(response.choices[0].message.tool_calls)
    )

    response = client.chat.complete(
        model=model, messages=messages, tools=tools, temperature=0,
    )

    print(response)
    print()
    print(f"Final answer:\n{response.choices[0].message.content}")


if __name__ == "__main__":
    main()
