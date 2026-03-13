import json
import os
import sentry_sdk

from wrapper.graph import build_graph
from langsmith import traceable
from Observablity.obs_manager import ObservabilityManager
from langfuse import Langfuse
from opentelemetry import trace


class LangGraphWrapper:

    def __init__(self, config_path, tool="none"):

        with open(config_path, "r") as f:
            self.config = json.load(f)

        self.graph = build_graph()

        self.pdf_path = None
        self.tool = tool

        self.obs = ObservabilityManager(tool)


    def load_pdf(self, pdf_path):

        self.pdf_path = pdf_path


    @traceable(name="rag_query")
    def ask(self, question):

        if not self.pdf_path:
            raise ValueError("PDF path is not set.")

        # open selected dashboard
        self.obs.start()

        state = {
            "pdf_path": self.pdf_path,
            "config": self.config,
            "question": question
        }

        # initialize langfuse client
        langfuse = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST")
        )

        tracer = trace.get_tracer("langgraph-rag")

        with sentry_sdk.start_transaction(op="rag_query", name="LangGraph RAG Query"):

            with langfuse.start_as_current_span(
                name="rag_query",
                input={"question": question}
            ) as lf_span:

                with tracer.start_as_current_span("rag_query") as otel_span:

                    result = self.graph.invoke(state)

                    lf_span.update(output={"answer": result["answer"]})

                    otel_span.set_attribute("answer", result["answer"])

                    sentry_sdk.capture_message(
                        f"RAG query executed: {question}"
                    )

        return result["answer"]