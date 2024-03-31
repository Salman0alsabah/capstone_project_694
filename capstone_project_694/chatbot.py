import os
from openai import OpenAI

class ChatBot:
    def __init__(self):
        self.previous_input = ""
        self.last_response = ""
        self.client = OpenAI(api_key="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")

    def ai_chat(self, chat_input):
        if chat_input != self.previous_input:
            try:
                response = self.client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": chat_input},
                        {"role": "assistant", "content": self.last_response}
                    ],
                    model="gpt-4-1106-preview"
                )
                # Adjust the response parsing based on the new structure
                if response and response.choices and len(response.choices) > 0:
                    self.last_response = response.choices[0].message.content.strip()
                else:
                    raise ValueError("Invalid response format or empty response")
                self.previous_input = chat_input
                print("ChatGPT:", self.last_response)
            except Exception as e:
                print(f"An error occurred: {e}")
                self.last_response = "Sorry, I couldn't process that. Please try again."

    def get_last_response(self):
        return self.last_response

