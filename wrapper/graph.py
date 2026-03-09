from langgraph.graph import StateGraph,START,END
from nodes.doc import load_split_doc
from nodes.llm import generate_answers
from nodes.retriver import retrive

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("load_doc",load_split_doc)
    graph.add_node("retrive_doc",retrive)
    graph.add_node("generate_answer",generate_answers)

    graph.add_edge(START, "load_doc")
    graph.add_edge("load_doc", "retrive_doc")
    graph.add_edge("retrive_doc", "generate_answer")
    graph.add_edge("generate_answer", END)


    return graph.compile()