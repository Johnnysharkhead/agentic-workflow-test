# LangGraph workflow construction

from langgraph.graph import StateGraph, START, END
from ..memory_LLMs_schema import AgentState
from ..agents import router_node, route_to_agent, calculator_agent, email_agent

# This is where LangGraph workflow comes in
def create_agent_graph():
    
    # instance a StateGraph with AgentState
    workflow = StateGraph(AgentState)
    
    # add nodes to the graph
    workflow.add_node("router", router_node)
    workflow.add_node("calculator_agent", calculator_agent)
    workflow.add_node("email_agent", email_agent)
    
    # Set the router node as START node
    workflow.add_edge(START, "router")
    
    # add conditional edges from the router to the two agents 
    workflow.add_conditional_edges(
        "router", 
        route_to_agent,
        {
            "calculator_agent": "calculator_agent", 
            "email_agent": "email_agent"
        }
    )
    
    # add edges from the agents to the END node
    workflow.add_edge("calculator_agent", END)
    workflow.add_edge("email_agent", END)

    """
    Take a user query as example, the workflow execution will be like this:

    [START]
        ↓
    [router node]
        ├─ Using LLM to analyze the user input and decide which agent to call
        ├─ Update state["next_agent"] = "calculator_agent"
        └─ Return the updated state
        ↓
    [Conditional Routing]
        ├─ Call the routing function route_to_agent(state), which reads state["next_agent"]
        ├─ routing function returns "calculator_agent"
        └─ Look up the mapping list: {"calculator_agent": "calculator_agent"}
        ↓
    [calculator_agent node]
        ├─ Receive the state, which contains the original user input and the router's decision
        ├─ Use the augmented LLM with tool calling to decide whether to call the calculator tool
        └─ Return the final answer to the states
        ↓
    [END]
    
    """

    # compile the workflow
    app = workflow.compile()
    
    return app
