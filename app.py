import streamlit as st
from google import genai


# -----------------------------
# Page settings
# -----------------------------

st.set_page_config(
    page_title="Minizo",
    page_icon="🤖",
    layout="centered"
)


# -----------------------------
# Create Gemini client
# -----------------------------

client = genai.Client()


# -----------------------------
# Minizo's personality
# -----------------------------

system_instruction = """
You are Minizo, a friendly AI chatbot.

Your personality:
- Be friendly, warm, and helpful.
- Explain things in simple language.
- Be encouraging when the user is learning.
- Keep answers clear and easy to understand.
- If you don't know something, say so honestly.
- Do not pretend to have personal experiences or feelings.
"""


# -----------------------------
# Store conversation
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Function to get Gemini response
# -----------------------------

def get_gemini_response(messages):

    conversation = []

    for message in messages:

        if message["role"] == "user":
            gemini_role = "user"
        else:
            gemini_role = "model"

        conversation.append(
            {
                "role": gemini_role,
                "parts": [
                    {
                        "text": message["content"]
                    }
                ]
            }
        )

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=conversation,
        config={
            "system_instruction": system_instruction
        }
    )

    return response.text


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.title("🤖 Minizo")

    st.write("Your friendly AI chatbot.")

    st.divider()

    st.subheader("✨ Features")

    st.write("💬 Chat with Gemini")
    st.write("🧠 Conversation memory")
    st.write("🗑️ Clear conversations")
    st.write("📚 Simple explanations")
    st.write("📥 Download conversations")
    st.write("🔄 Regenerate responses")

    st.divider()


    # -----------------------------
    # Clear Chat
    # -----------------------------

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    # -----------------------------
    # Download conversation
    # -----------------------------

    if st.session_state.messages:

        chat_text = ""

        for message in st.session_state.messages:

            if message["role"] == "user":

                chat_text += (
                    f"You:\n"
                    f"{message['content']}\n\n"
                )

            else:

                chat_text += (
                    f"Minizo:\n"
                    f"{message['content']}\n\n"
                )


        st.download_button(
            label="📥 Download Chat",
            data=chat_text,
            file_name="minizo_chat.txt",
            mime="text/plain",
            use_container_width=True
        )


    st.divider()

    st.caption("Minizo v0.1")


# -----------------------------
# Main page
# -----------------------------

st.title("🤖 kudos ...Minizo here!!")


# -----------------------------
# Welcome screen
# -----------------------------

if not st.session_state.messages:

    st.markdown(
        """
        ### 👋 Hey! I'm Minizo

        Your friendly AI chatbot.

        Ask me anything, learn something new,
        or just have a conversation with me!
        """
    )

    st.divider()

    st.subheader("💡 Try asking me")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🐍 Learn Python")

    with col2:
        st.info("💻 Debug my code")

    with col3:
        st.info("🧠 Explain a concept")


# -----------------------------
# Display messages
# -----------------------------

for index, message in enumerate(
    st.session_state.messages
):

    with st.chat_message(message["role"]):

        st.write(message["content"])


        # -----------------------------
        # Regenerate button
        # -----------------------------

        if (
            message["role"] == "assistant"
            and index == len(st.session_state.messages) - 1
        ):

            if st.button(
                "🔄 Regenerate Response",
                key="regenerate"
            ):

                # Remove old response
                st.session_state.messages.pop()

                try:

                    new_response = get_gemini_response(
                        st.session_state.messages
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": new_response
                        }
                    )

                except Exception:

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": (
                                "I'm temporarily unable to respond "
                                "because the Gemini API quota has "
                                "been reached. Please try again later."
                            )
                        }
                    )

                st.rerun()


# -----------------------------
# Chat input
# -----------------------------

user_message = st.chat_input(
    "Talk to Minizo..."
)


# -----------------------------
# New user message
# -----------------------------

if user_message:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # Display user message
    with st.chat_message("user"):

        st.write(user_message)


    # Get Gemini response
    try:

        response_text = get_gemini_response(
            st.session_state.messages
        )

    except Exception:

        response_text = (
            "I'm temporarily unable to respond because "
            "the Gemini API quota has been reached. "
            "Please try again later."
        )


    # Display response
    with st.chat_message("assistant"):

        st.write(response_text)


    # Save response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_text
        }
    )