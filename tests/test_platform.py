
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wrapper.wrapper import LangGraphWrapper
rag = LangGraphWrapper("config/config.json")

rag.load_pdf("C:/Users/Rishika Gaja/Downloads/Tools.pdf")

print(rag.ask("What is this document about?"))