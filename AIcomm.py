# Importar la biblioteca OpenAI
from openai import OpenAI

# Configurar el cliente de OpenAI con la URL base y la clave API de NVIDIA
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

class ConversationMemory:
    """Clase para manejar el historial de la conversación."""

    def __init__(self):
        """Inicializar la clase con una lista vacía para el historial."""
        self.history = []

    def add_message(self, role, content):
        """
        Añadir un mensaje al historial.
        
        Args:
            role (str): El rol del mensaje (usuario o asistente).
            content (str): El contenido del mensaje.
        """
        self.history.append({"role": role, "content": content})

    def get_context(self):
        """Obtener todo el historial de la conversación."""
        return self.history

# Crear una instancia de ConversationMemory
memory = ConversationMemory()

def handle_conversation(user_input):
    """
    Manejar una interacción de la conversación.

    Args:
        user_input (str): La entrada del usuario.

    Returns:
        str: La respuesta del asistente AI, o None si hay un error.
    """
    # Añadir el mensaje del usuario al historial
    memory.add_message("user", user_input)

    # Obtener el contexto completo de la conversación
    context = memory.get_context()

    try:
        # Crear una solicitud de completación de chat
        completion = client.chat.completions.create(
            model="meta/llama3-70b-instruct",
            messages=context,
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=True
        )

        # Procesar la respuesta por partes
        ai_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                ai_response += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="")

        # Añadir la respuesta del asistente al historial
        memory.add_message("assistant", ai_response)

        return ai_response

    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return None

'''
Bucle para solicitar y procesar 4 prompts (comentado)
for i in range(4):
    user_input = input(f"Ingresa el prompt {i+1}: ")
    response = handle_conversation(user_input)
    print("\nRespuesta:", response, "\n")
'''
