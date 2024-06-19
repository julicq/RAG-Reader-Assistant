import streamlit as st
from main_logic import parse_file, get_embeddings, get_response

def main():
    st.title("Text Analysis and Q&A")

    uploaded_file = st.file_uploader("Choose a file", type=["txt", "pdf", "doc", "docx"])
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]
        temp_filename = f"uploaded_file.{file_extension}"
        
        with open(temp_filename, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        paragraphs = parse_file(temp_filename)
        embeddings = get_embeddings(temp_filename, "nomic-embed-text", paragraphs)

        prompt = st.text_input("What do you want to know?")
        if st.button("Submit"):
            if prompt:
                response = get_response(paragraphs, embeddings, prompt)
                st.write("Response:")
                st.write(response)
            else:
                st.write("Please enter a prompt")

if __name__ == "__main__":
    main()
