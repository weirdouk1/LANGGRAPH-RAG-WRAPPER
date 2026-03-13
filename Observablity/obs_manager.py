import os
import subprocess
from time import time
import webbrowser


class ObservabilityManager:

    def __init__(self, tool):

        self.tool = tool

    def start(self):

        if self.tool == "langsmith":
            os.environ["LANGCHAIN_TRACING_V2"] = "true"
            os.environ["LANGCHAIN_PROJECT"] = "langgraph-rag-wrapper"
            webbrowser.open("https://smith.langchain.com")

        elif self.tool == "phoenix":
            webbrowser.open("http://localhost:6006")

        elif self.tool == "langfuse":
            from langfuse import Langfuse
            import os
            self.langfuse = Langfuse(
                public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
                secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
                host  = os.getenv("LANGFUSE_HOST")
            )
            webbrowser.open("https://us.cloud.langfuse.com")

        elif self.tool == "sentry":
            import sentry_sdk
            import os
            sentry_sdk.init(
                dsn=os.getenv("SENTRY_DSN"),
                traces_sample_rate=1.0
            )
            webbrowser.open("https://sentry.io")

        elif self.tool == "otel":
            webbrowser.open("http://localhost:16686")