import streamlit as st
from main_logic import parse_file, get_embeddings, get_response
import time

def main():
    st.title("Text Analysis and Q&A Bot")

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
        for chat in st.session_state.chat_history:
            st.write(f"**User:** {chat['user']}")
            st.write(f"**Bot:** {chat['bot']}")
            st.write("---")

if __name__ == "__main__":
    main()
