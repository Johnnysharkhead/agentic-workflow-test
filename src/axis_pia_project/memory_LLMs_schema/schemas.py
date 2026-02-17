# Pydantic schemas for LLMs structured outputs

from pydantic import BaseModel, Field
from typing import Literal

# Need to verify the output of the router node is valid and can be parsed, so we define a structured output schema for the router's decision. 
class RouterDecision(BaseModel):
    """Schema for router's decision on which agent to use."""
    
    # ensure that the agent_name is either "calculator_agent" or "email_agent"（Node name）
    agent_name: Literal["calculator_agent", "email_agent"] = Field(
        description="The name of the agent to handle the user's request"
    )
    # enable the router to provide reasoning for its choice (for monitoring)
    reasoning: str = Field(
        description="Brief explanation of why this agent was chosen"
    )
