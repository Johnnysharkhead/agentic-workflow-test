# State definitions for LangGraph (Short-term memory of the agents)
# Note: This matters a lot for the workflow design!

from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from typing import Annotated
import operator

# Graph state
class AgentState(TypedDict):
    # operator.add ensures that the messages list can be appended with new messages as the conversation progresses, which is essential for maintaining the context of the dialogue across different nodes in the graph.
    
    """
    BaseMessage
    ├── HumanMessage      # User Input
    ├── SystemMessage     # AI Instruction
    ├── AIMessage         # AI Inference Response
    └── ToolMessage       # Tool Calling Response
    """
    messages: Annotated[list[BaseMessage], operator.add] 

    next_agent: str  
    final_answer: str
