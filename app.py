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

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

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

        Ask me anything, learn something new, or just have a conversation with me!
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
# Display previous messages
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# -----------------------------
# Chat input
# -----------------------------

user_message = st.chat_input("Talk to Minizo...")


# -----------------------------
# Talk to Gemini
# -----------------------------

if user_message:

    # Save user's message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    # Display user's message
    with st.chat_message("user"):
        st.write(user_message)


    # -----------------------------
    # Convert conversation for Gemini
    # -----------------------------

    conversation = []

    for message in st.session_state.messages:

        if message["role"] == "user":
            gemini_role = "user"
        else:
            gemini_role = "model"

        conversation.append({
            "role": gemini_role,
            "parts": [
                {
                    "text": message["content"]
                }
            ]
        })


    # -----------------------------
    # Send conversation to Gemini
    # -----------------------------

    try:

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=conversation,
            config={
                "system_instruction": system_instruction
            }
        )

        response_text = response.text

    except Exception:

        response_text = (
            "I'm temporarily unable to respond because the Gemini API "
            "quota has been reached. Please try again later."
        )


    # -----------------------------
    # Display Minizo's response
    # -----------------------------

    with st.chat_message("assistant"):
        st.write(response_text)


    # -----------------------------
    # Save Minizo's response
    # -----------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })