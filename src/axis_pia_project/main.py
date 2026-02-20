"""
Trying to build a skeleton for the Axis project, which implement a router and 2 agent(connect to the router), using LangGraph.
The router will receive the user input and decide which agent to call, and the agent will call its own tools to get the answer, then return to the router, and the router will return the final answer.
"""

from axis_pia_project.graph_workflow import create_agent_graph
from langchain_core.messages import HumanMessage



def main():
    
    app = create_agent_graph()
 
    # case1: calulate a math problem
    result1 = app.invoke({
        "messages": [HumanMessage(content="Help me to calculate (25 + 75) * 3 / 2")],
        "next_agent": "",
        "final_answer": ""
    })
    
    print(f"\n The case 1 final answer is : {result1['final_answer']}\n")
    
    # case2: query product info based on itemId, which is for testing the routing and tool calling of the calculator_agent
    
    result2 = app.invoke({
        "messages": [HumanMessage(content="I want to know about the main info of the product with itemId 68003")],
        "next_agent": "",
        "final_answer": ""
    })
    
    print(f"\n The case 2 final answer is:\n{result2['final_answer']}\n")
 

if __name__ == "__main__":
    main()
