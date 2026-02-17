# Axis PIA Project

A LangGraph-based multi-agent system with intelligent routing capabilities.

## Overview

This project implements a router-agent architecture using LangGraph, where user queries are dynamically routed to specialized agents based on their content.

## System Architecture

```
┌─────────────┐
│   User      │
│   Input     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│         Router Node                 │
│  (LLM-powered query analysis)       │
└──────────┬──────────────────────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌────────┐   ┌────────┐
│Calculator│   │ Email  │
│ Agent   │   │ Agent  │
│(Math)   │   │(Writing)│
└────┬────┘   └────┬────┘
     │             │
     └──────┬──────┘
            ▼
      ┌──────────┐
      │ Response │
      └──────────┘
```

### Components

- **Router Node**: Analyzes user input and routes to appropriate agent
- **Calculator Agent**: Handles mathematical calculations using tool calling
- **Email Agent**: Generates professional emails and formal documents
- **Graph Workflow**: Orchestrates the multi-agent flow with LangGraph

### Project Structure

```
src/axis_pia_project/
├── agents/              # Agent implementations
│   ├── router.py        # Routing logic
│   ├── calculator_agent.py
│   └── email_agent.py
├── config/              # LLM configuration
├── graph_workflow/      # LangGraph workflow
├── memory_LLMs_schema/  # Pydantic schemas & state definitions
├── tools/               # Agent tools (calculator)
└── main.py              # Entry point
```

## Installation

```bash
# Install dependencies
uv sync

# Or with pip
pip install -e .
```

## Configuration

Create a `.env` file with your API credentials:

```env
AXIS_DEV_API_KEY=your_api_key_here
```

## Requirements

See `pyproject.toml` for complete dependencies.
