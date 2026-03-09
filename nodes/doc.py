from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_split_doc(state):
    pdf_path = state["pdf_path"]
    config = state["config"]
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=config["chunk_size"], chunk_overlap=config["chunk_overlap"])
    split_docs = splitter.split_documents(docs)
    state["documents"] = split_docs
    return state
