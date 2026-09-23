from google import genai

client = genai.Client()

chat = client.chats.create(
    model="gemini-3-flash-preview"
)

while True:
    user_message = input("You: ")

    if user_message.lower() == "quit":
        print("Goodbye!")
        break

    response = chat.send_message(
        message=user_message
    )

    print("AI:", response.text)