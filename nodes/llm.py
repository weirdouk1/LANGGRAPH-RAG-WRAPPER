from langchain_ollama.llms import OllamaLLM 
from langchain_core.prompts import ChatPromptTemplate

def generate_answers(state):
    question = state["question"]
    context_docs = state["context_docs"]
    config = state["config"]
    
    context = "\n\n".join([doc.page_content for doc in context_docs])
    template = f"""
you are an expert assistant that answers questions using the uploaded pdf

if the answer is present in the document say:
"from the document:" and then answer

if the answer is not present say:
"I could not find the answer in the uploaded pdf, but generally:" and then answer using your knowledge
Document Content:
{context}
Question:
{question}
"""
    prompt = ChatPromptTemplate.from_template(template)
    model = OllamaLLM(model=config["llm_model"])
    chain = prompt | model
    answer = chain.invoke({"context_docs": context, "question": question})
    state["answer"] = answer
    return state