import streamlit as st
from google import genai


# -----------------------------
# Page settings
# -----------------------------

st.set_page_config(
    page_title="Minizo",
    page_icon="🤖"
)

st.title("🤖 kudos ...Minizo here!!")
st.write("Chat with Gemini!")


# -----------------------------
# Clear Chat button
# -----------------------------

if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# -----------------------------
# Create Gemini client
# -----------------------------

client = genai.Client()


# -----------------------------
# Store conversation
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Display previous messages
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# -----------------------------
# Get user's message
# -----------------------------

user_message = st.chat_input("Type your message...")


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

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=conversation
    )


    # -----------------------------
    # Display Minizo's response
    # -----------------------------

    with st.chat_message("assistant"):
        st.write(response.text)


    # -----------------------------
    # Save Minizo's response
    # -----------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": response.text
    })