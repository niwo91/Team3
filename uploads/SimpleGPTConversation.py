import openai
from openai import OpenAI
import sys
import os
import textwrap

def pretty_print(text, width=80):
    """
    Format and print text with line breaks at a specified width.
    """
    wrapped_text = textwrap.fill(text, width)
    print(wrapped_text)

client = OpenAI(
    api_key=os.environ.get("OPENAI_KEY"),  # This is the default and can be omitted
)

def chat_with_openai():
    print("Start chatting with the bot (type 'exit' to stop):")

    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_input,
                }
            ],
            model="gpt-4o",
            max_tokens=300,
            temperature=0.7,
        )
        # Get the bot's response from the API call
        bot_response = response.choices[0].message.content.strip()
        pretty_print(f"Chatbot: {bot_response}", 50)

# Run the chatbot
chat_with_openai()
