"""
Trying to build a skeleton for the Axis project, which implement a router and 2 agent(connect to the router), using LangGraph.
The router will receive the user input and decide which agent to call, and the agent will call its own tools to get the answer, then return to the router, and the router will return the final answer.
"""

from axis_pia_project.graph_workflow import create_agent_graph
from langchain_core.messages import HumanMessage



def main():
    
    app = create_agent_graph()
    
    """
    # case1: calulate a math problem
    result1 = app.invoke({
        "messages": [HumanMessage(content="Help me to calculate (25 + 75) * 3 / 2")],
        "next_agent": "",
        "final_answer": ""
    })
    
    print(f"\n The case 1 final answer is : {result1['final_answer']}\n")
    """
    
    # case2: query product info based on itemId, which is for testing the routing and tool calling of the calculator_agent
    
    result2 = app.invoke({
        "messages": [HumanMessage(content="Which Power Supplies are compatible with the M5000? ")],
        "next_agent": "",
        "final_answer": ""
    })
    
    print(f"\n{result2['messages'][-1].content}\n{result2['final_answer']}\n")


    result3 = app.invoke({
        "messages": [HumanMessage(content=" What is the correct part number for the Q6074-E without the mid-span?")],
        "next_agent": "",
        "final_answer": ""
    })
    
    print(f"\n{result3['messages'][-1].content}\n{result3['final_answer']}\n")
   
 

if __name__ == "__main__":
    main()
