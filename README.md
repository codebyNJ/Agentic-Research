# Develop an AI agent using SmolAgent Framework that uses ReAct(Reason - Act) feedback system with deep research capabilities that can be easily used by users to tackle real world problems in a faster method.

## Langfuse-Powered Smolagents with Hugging Face

### Overview

This project integrates [Langfuse](https://langfuse.com/) with [Smolagents](https://github.com/smol-ai/smolagents) to monitor and improve reasoning and decision-making capabilities when executing multi-step tasks. By utilizing OpenTelemetry tracing and AI models from Hugging Face, this implementation allows real-time performance tracking and optimization of autonomous agents.

### Features

- **Langfuse Integration**: Observability with OpenTelemetry.
- **Hugging Face AI Model**: Uses `Qwen/Qwen2.5-Coder-32B-Instruct`.
- **Multi-Agent System**: Implements `CodeAgent` and `ToolCallingAgent`.
- **Web Search & Data Retrieval**: DuckDuckGo and Webpage visiting tools.
- **Replay Functionality**: Allows re-execution of previous runs.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Hugging Face API key
- Langfuse Public and Secret Keys

### Installation

```
pip install smolagents opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
```


### Environment Variables

Set up the required environment variables:

```python
import os
import base64

LANGFUSE_PUBLIC_KEY="pk-..."
LANGFUSE_SECRET_KEY="sk-..."
LANGFUSE_AUTH=base64.b64encode(f"{LANGFUSE_PUBLIC_KEY}:{LANGFUSE_SECRET_KEY}".encode()).decode()

os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://us.cloud.langfuse.com/api/public/otel"
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"
os.environ["HF_TOKEN"] = "hf_..."

```

### Running the Project

```
from smolagents import CodeAgent, ToolCallingAgent, DuckDuckGoSearchTool, VisitWebpageTool, HfApiModel
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from openinference.instrumentation.smolagents import SmolagentsInstrumentor
```

### Setup tracing

```
trace_provider = TracerProvider()
trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter()))
SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)
```

### Initialize model
```
model = HfApiModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
```

### Define agents
```
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
```


### Execute agent task

```
manager_agent.run("How can Langfuse be used to monitor and improve the reasoning and decision-making of smolagents when they execute multi-step tasks?")
```

<!-- ## License
This project is open-source and available for modification and contribution. Feel free to fork and enhance it! -->

