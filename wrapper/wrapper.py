import json
from wrapper.graph import build_graph

class LangGraphWrapper:
    def __init__(self, config_path):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.graph = build_graph()
        self.pdf_path = None

    def load_pdf(self, pdf_path):
        self.pdf_path = pdf_path
    
    def ask(self, question):
        if not self.pdf_path:
            raise ValueError("PDF path is not set. Please load a PDF first.")
        
        state = {
            "pdf_path": self.pdf_path,
            "config": self.config,
            "question": question
        }
        result = self.graph.invoke(state)
        return result["answer"]