import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from wrapper.wrapper import LangGraphWrapper

app = FastAPI()

rag = LangGraphWrapper("config/config.json")

rag.load_pdf("C:/Users/Rishika Gaja/Downloads/Tools.pdf")


@app.get("/rag/query")
def query(question: str):

    answer = rag.ask(question)

    return {"answer": answer}