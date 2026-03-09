from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

def retrive(state):
    docs = state["documents"]
    config = state["config"]
    question = state["question"]
    embeddings = OllamaEmbeddings(model=config["embedding_model"])
    db_location = "./chroma_langchain_db"

    vector_store = Chroma.from_documents(docs, embedding=embeddings, persist_directory=db_location)
    ids = []

    for i, doc in enumerate(docs):
        doc.id = str(i)
        ids.append(str(i))

    vector_store.add_documents(docs, ids=ids)
    retriever = vector_store.as_retriever(search_kwargs={"k": config["retrive_k"]})
    retrive_docs = retriever.invoke(question)
    state["context_docs"] = retrive_docs
    return state