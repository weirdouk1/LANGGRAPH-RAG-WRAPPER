from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import phoenix as px
import sentry_sdk

from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import sentry_sdk

from openinference.instrumentation.langchain import LangChainInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

# Jaeger exporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Phoenix exporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter as HTTPExporter

from opentelemetry import trace


# --------------------------------
# OBSERVABILITY SETUP
# --------------------------------

if "otel_initialized" not in st.session_state:

    tracer_provider = TracerProvider()

    # Jaeger exporter (gRPC)
    jaeger_exporter = OTLPSpanExporter(
        endpoint="http://127.0.0.1:4317",
        insecure=True
    )

    # Phoenix exporter (HTTP)
    phoenix_exporter = HTTPExporter(
        endpoint="http://127.0.0.1:6006/v1/traces"
    )

    tracer_provider.add_span_processor(SimpleSpanProcessor(jaeger_exporter))
    tracer_provider.add_span_processor(SimpleSpanProcessor(phoenix_exporter))

    trace.set_tracer_provider(tracer_provider)

    LangChainInstrumentor().instrument()

    st.session_state["otel_initialized"] = True


# --------------------------------
# NOW IMPORT APP MODULES
# --------------------------------

from wrapper.wrapper import LangGraphWrapper

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=1.0
)

# --------------------------------
# STREAMLIT UI
# --------------------------------

st.title("LangGraph RAG Observability")

tool = st.selectbox(
    "Select Observability Tool",
    ["none","langsmith","phoenix","langfuse","sentry","otel"]
)

pdf = st.file_uploader("Upload PDF")

question = st.text_input("Ask a question")

# --------------------------------
# EXECUTION
# --------------------------------

if st.button("Ask"):

    if pdf is None:
        st.error("Upload PDF first")

    else:

        with open("temp.pdf","wb") as f:
            f.write(pdf.read())

        rag = LangGraphWrapper("config/config.json", tool)

        rag.load_pdf("temp.pdf")

        answer = rag.ask(question)

        st.subheader("Answer")
        st.write(answer)