import streamlit as st
from main_logic import parse_file, get_embeddings, get_response
import time

def main():
    st.title("Text Analysis and Q&A Bot")

    # Custom CSS
    st.markdown(
        """
        <style>
        .chat-container {
            background-color: #f0f0f5;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .chat-message {
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
        }
        .chat-message.user {
            background-color: #d1e7dd;
            text-align: right;
        }
        .chat-message.bot {
            background-color: #fff3cd;
        }
        .chat-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "doc", "docx"])
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]
        temp_filename = f"uploaded_file.{file_extension}"
        
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write("File uploaded successfully.")
        progress_bar = st.progress(0)

        # Parse file and display progress
        paragraphs = parse_file(temp_filename)
        progress_bar.progress(30)

        # Generate embeddings and display progress
        embeddings = get_embeddings(temp_filename, "nomic-embed-text", paragraphs)
        progress_bar.progress(60)

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        def handle_query():
            user_query = st.session_state.user_input
            if user_query:
                response = get_response(paragraphs, embeddings, user_query)
                st.session_state.chat_history.append({"user": user_query, "bot": response})
                st.session_state.user_input = ""
                progress_bar.progress(100)

        st.text_input("What do you want to know?", key="user_input", on_change=handle_query)

        # Display chat history
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            st.markdown(f"<div class='chat-message user'>{chat['user']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-message bot'>{chat['bot']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
