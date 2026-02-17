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
    
    # case2: write an email
    result2 = app.invoke({
        "messages": [HumanMessage(content="I would like to write an email to my supervisor to request a day off.")],
        "next_agent": "",
        "final_answer": ""
    })
    
    print(f"\n The case 2 final answer is:\n{result2['final_answer']}\n")
    
    # case3: write an email with calculation involved (to test the routing)
    result3 = app.invoke({
        "messages": [HumanMessage(content="I need to write an email to my supervisor to tell him that what's the result of 1+2+3+...+100.")],
        "next_agent": "",
        "final_answer": ""
    })
    
    print(f"\n The case 3 final answer is:\n{result3['final_answer']}\n")
   

    # case4: write random question neither related to calculation nor email, to see how the router and agents handle it (edge case)
    result4 = app.invoke({
        "messages": [HumanMessage(content="why cloud seems blue?")],
        "next_agent": "",
        "final_answer": ""
    })
    
    print(f"\n The case 4 final answer is:\n{result4['final_answer']}\n")


if __name__ == "__main__":
    main()
