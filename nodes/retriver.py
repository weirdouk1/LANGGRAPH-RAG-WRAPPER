from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import os


def retrive(state):

    docs = state["documents"]
    config = state["config"]
    question = state["question"]

    embeddings = OllamaEmbeddings(model=config["embedding_model"])

    db_location = "./chroma_langchain_db"

    # If vector DB already exists → load it
    if os.path.exists(db_location):

        vector_store = Chroma(
            persist_directory=db_location,
            embedding_function=embeddings
        )

    else:

        vector_store = Chroma.from_documents(
            docs,
            embedding=embeddings,
            persist_directory=db_location
        )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": config["retrive_k"]}
    )

    retrieve_docs = retriever.invoke(question)

    state["context_docs"] = retrieve_docs

    return state