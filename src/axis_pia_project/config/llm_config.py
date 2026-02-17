"""LLM configuration for the Axis project."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Initialize LangChain ChatOpenAI for LangGraph agents
# This wraps the Axis API in a LangChain-compatible interface
llm_from_axis = ChatOpenAI(
    model="prisma_gemini_pro",
    base_url="https://api-dev.ai.auth.axis.cloud/v1",  # Changed from openai_api_base
    api_key = os.getenv("AXIS_DEV_API_KEY"),  # Changed from openai_api_key
    temperature=0.1,
    max_tokens=300
)
