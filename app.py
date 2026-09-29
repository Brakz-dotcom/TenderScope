import os
import streamlit as st
import pymupdf as fitz
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(page_title="Document & Contract Auditor", layout="wide")
st.title("📄 Smart Document & Contract Auditor")
st.caption("Multimodal RAG with Grounded Source Citations")

# Initialize session state keys
if "selected_query" not in st.session_state:
    st.session_state.selected_query = ""
if "current_file" not in st.session_state:
    st.session_state.current_file = None

# Sidebar for file upload & presets
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Upload a PDF (Contract, Tender, or Spec Sheet)", type=["pdf"])
    
    st.markdown("---")
    st.subheader("⚡ Quick Audit Presets")

    if st.button("🔍 Check Penalties & Delay"):
        st.session_state.selected_query = "What are the liquidated damages and delay penalties?"

    if st.button("🛠️ Check Maintenance & Fuel"):
        st.session_state.selected_query = "Who pays for site insurance, fuel, and daily maintenance?"

    if st.button("📦 Equipment Scope & Term"):
        st.session_state.selected_query = "What equipment is being leased, and what is the lease term?"

def extract_pdf_data(uploaded_file):
    """Extracts text page by page with explicit page number metadata."""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    pages_data = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        if text.strip():
            pages_data.append({
                "text": text,
                "metadata": {"page": page_num + 1, "source": uploaded_file.name}
            })
    return pages_data

def format_docs(docs):
    """Combines retrieved document chunks into formatted context."""
    return "\n\n".join(f"[Page {d.metadata.get('page', 'Unknown')}]:\n{d.page_content}" for d in docs)

# Indexing Pipeline
if uploaded_file and groq_api_key:
    # Reset index if a new file is uploaded
    if st.session_state.current_file != uploaded_file.name:
        with st.spinner("Parsing document and indexing vector embeddings..."):
            pages_data = extract_pdf_data(uploaded_file)
            
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
            all_chunks = []
            all_metadatas = []
            
            for item in pages_data:
                splits = text_splitter.split_text(item["text"])
                all_chunks.extend(splits)
                all_metadatas.extend([item["metadata"]] * len(splits))
            
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            st.session_state.vector_store = Chroma.from_texts(
                texts=all_chunks,
                embedding=embeddings,
                metadatas=all_metadatas
            )
            st.session_state.current_file = uploaded_file.name
        st.success(f"Indexed {len(all_chunks)} chunks from {uploaded_file.name} successfully!")

    # Question Answering Section
    query = st.text_input(
        "Ask a question or audit a clause (e.g., 'What are the penalty terms?'):",
        value=st.session_state.selected_query
    )    
    
    if query and "vector_store" in st.session_state:
        with st.spinner("Analyzing document..."):
            retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
            
            llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name="openai/gpt-oss-120b",
                temperature=0
            )
            
            system_prompt = (
                "You are an expert contract and tender compliance auditor.\n"
                "Answer the user's question strictly using the provided context chunks below.\n"
                "For every finding, cite the exact page number in the format: [Source: Page X].\n"
                "If the information is not present in the context, state clearly that it is not specified in the document.\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}"
            )
            
            prompt = ChatPromptTemplate.from_template(system_prompt)
            
            rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )
            
            answer = rag_chain.invoke(query)
            retrieved_docs = retriever.invoke(query)
            
            st.subheader("Audit Finding:")
            st.write(answer)
            
            with st.expander("Inspect Retrieved Source Passages"):
                seen_content = set()
                for doc in retrieved_docs:
                    if doc.page_content not in seen_content:
                        seen_content.add(doc.page_content)
                        page_num = doc.metadata.get("page", 1)
                        st.markdown(f"**Page {page_num}**")
                        st.text(doc.page_content)
                        st.markdown("---")

elif not groq_api_key:
    st.warning("Please ensure GROQ_API_KEY is properly set in your .env file.")