import streamlit as st
from main_logic import parse_file, get_embeddings, get_response
import time

def main():
    st.title("Text Analysis and Q&A")

    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "doc", "docx"])
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]
        temp_filename = f"uploaded_file.{file_extension}"
        
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write("File uploaded successfully.")
        st.progress(0)

        # Parse file and display progress
        paragraphs = parse_file(temp_filename)
        st.progress(30)

        # Generate embeddings and display progress
        embeddings = get_embeddings(temp_filename, "nomic-embed-text", paragraphs)
        st.progress(60)

        # Accept user prompt
        prompt = st.text_input("What do you want to know?")
        if st.button("Submit"):
            if prompt:
                # Get response and display progress
                response = get_response(paragraphs, embeddings, prompt)
                st.progress(90)
                st.write("Response:")
                st.write(response)
                st.progress(100)
            else:
                st.write("Please enter a prompt")

if __name__ == "__main__":
    main()
