import os
import base64

#Langfuse API Key

LANGFUSE_PUBLIC_KEY="pk-lf-06fd2f47-a6be-4053-adbf-a54a70da4011"
LANGFUSE_SECRET_KEY="sk-lf-6330a411-d6a0-4c0a-a485-a5b11eb46a80"
LANGFUSE_AUTH=base64.b64encode(f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}".encode()).decode()

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://us.cloud.langfuse.com/api/public/otel" # US data region
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

# your Hugging Face token
os.environ["HF_TOKEN"] = "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"

from opentelemetry.sdk.trace import TracerProvider

from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

trace_provider = TracerProvider()
trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))

SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)

from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    DuckDuckGoSearchTool,
    VisitWebpageTool,
    HfApiModel,
)

#model name
model = HfApiModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct"
)

search_agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool(), VisitWebpageTool()],
    model=model,
    name="search_agent",
    description="This is an agent that can do web search.",
)

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[search_agent],
)
manager_agent.run(
    "Renewable energy for urban areas"
)

#manager_agent.replay() to replay the pervious run of the agent.