import streamlit as st
from google import genai


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Minizo",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client()


# ============================================================
# MINIZO PERSONALITY
# ============================================================

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


# ============================================================
# CONVERSATION MEMORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# GET RESPONSE FROM GEMINI
# ============================================================

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


# ============================================================
# SEND A MESSAGE
# ============================================================

def send_message(user_message):

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

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

    # Save Minizo response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response_text
        }
    )


# ============================================================
# SIDEBAR
# ============================================================

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


    # ========================================================
    # CLEAR CHAT
    # ========================================================

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


    # ========================================================
    # DOWNLOAD CHAT
    # ========================================================

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


# ============================================================
# MAIN TITLE
# ============================================================

st.title("🤖 kudos ...Minizo here!!")


# ============================================================
# WELCOME SCREEN
# ============================================================

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


    # ========================================================
    # SUGGESTED PROMPT BUTTONS
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # LEARN PYTHON
    # --------------------------------------------------------

    with col1:

        if st.button(
            "🐍 Learn Python",
            use_container_width=True
        ):

            send_message(
                "Teach me Python from the absolute beginner level. "
                "Explain it simply and give me a small example."
            )

            st.rerun()


    # --------------------------------------------------------
    # DEBUG CODE
    # --------------------------------------------------------

    with col2:

        if st.button(
            "💻 Debug my code",
            use_container_width=True
        ):

            send_message(
                "I want help debugging my code. "
                "Please ask me to paste my code and explain "
                "what error or problem I am facing."
            )

            st.rerun()


    # --------------------------------------------------------
    # EXPLAIN CONCEPT
    # --------------------------------------------------------

    with col1:

        if st.button(
            "🧠 Explain a concept",
            use_container_width=True
        ):

            send_message(
                "I want to learn a concept. "
                "Please ask me which concept I want explained, "
                "then explain it in very simple language with "
                "an example."
            )

            st.rerun()


    # --------------------------------------------------------
    # STUDY HELP
    # --------------------------------------------------------

    with col2:

        if st.button(
            "📚 Help me study",
            use_container_width=True
        ):

            send_message(
                "Help me study. Ask me what subject or topic "
                "I am studying and then help me learn it step "
                "by step using simple explanations."
            )

            st.rerun()


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for index, message in enumerate(
    st.session_state.messages
):

    with st.chat_message(message["role"]):

        st.write(message["content"])


        # ====================================================
        # REGENERATE LAST RESPONSE
        # ====================================================

        if (
            message["role"] == "assistant"
            and index == len(st.session_state.messages) - 1
        ):

            if st.button(
                "🔄 Regenerate Response",
                key="regenerate_response"
            ):

                # Remove previous AI response
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


# ============================================================
# CHAT INPUT
# ============================================================

user_message = st.chat_input(
    "Talk to Minizo..."
)


# ============================================================
# HANDLE USER MESSAGE
# ============================================================

if user_message:

    send_message(user_message)

    st.rerun()