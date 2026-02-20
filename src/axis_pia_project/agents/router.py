"""Router node and routing logic."""

from typing import Literal
from langchain_core.messages import SystemMessage
from ..config import llm_from_axis
from ..memory_LLMs_schema import AgentState, RouterDecision

# Build the Nodes
# Note:all node input comes from the AgentState, and all node output is also updating the AgentState, which will be passed to the next node.

# Node 1: Router Node
def router_node(state: AgentState) -> AgentState:
    """Navigate the user input to the right agent based on the content of the message."""
    
    # structured output ensures the router's decision can be parsed and monitored,implemented by the RouterDecision pydantic model, which defines the expected output format of the router node, including the agent name and reasoning for monitoring purposes.
    llm = llm_from_axis.with_structured_output(RouterDecision) 

    # prompt of the router node
    router_prompt = """You are an intelligent router that directs user queries to the appropriate agent. You have two agents available:
    
    - calculator_agent: solves math and product query problems based on itemId
    - email_agent: writes emails, letters, and formal documents
    
    User input: {input}
    
    Analyze the user's request and select the most appropriate agent. If the request doesn't fit either agent well, choose email_agent as the default.
    Respond with ONLY the agent name at the beginning: either "calculator_agent" or "email_agent".
    """

    user_input = state["messages"][-1].content
    
    # Invoke the LLM to get the router's decision on which agent to use
    response = llm.invoke([
        SystemMessage(content=router_prompt.format(input=user_input))
    ])
    
    agent_name = response.agent_name
    reasoning = response.reasoning
    

    # To see the response from the router node
    print(f"\n Router decision is: {agent_name}")
    print(f"Why the router made this decision is: {reasoning}\n")
    
    return {
        **state, # keep the existing state fields
        "next_agent": agent_name # guaranteed to be valid agent name
    }

# Routing Function
# Define how the router node routes to the next node(next agent) based on the content of user input. 
def route_to_agent(state: AgentState) -> Literal["calculator_agent", "email_agent"]:
    """Return the next agent name based on the content of user input."""
    
    # this varibale is defined in the AgentState TypedDict, and will be updated by the router_node
    next_agent = state.get("next_agent", "")
    
    if "calculator" in next_agent:
        return "calculator_agent"
    elif "email" in next_agent:
        return "email_agent"
    else:
        # default setting, in case the router node fails
        return "email_agent"
