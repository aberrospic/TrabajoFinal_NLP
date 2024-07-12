from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

class ConversationMemory:
    def __init__(self):
        self.history = []

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

    def get_context(self):
        return self.history

memory = ConversationMemory()

def handle_conversation(user_input):
    memory.add_message("user", user_input)

    context = memory.get_context()

    try:
        completion = client.chat.completions.create(
            model="meta/llama3-70b-instruct",
            messages=context,
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=True
        )

        ai_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                ai_response += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="")

        memory.add_message("assistant", ai_response)

        return ai_response

    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return None