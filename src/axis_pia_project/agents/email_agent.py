"""Email agent node."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from ..memory_LLMs_schema import AgentState

# Load environment variables
load_dotenv()

# Node 3: Email Agent (without tool calling)
def email_agent(state: AgentState) -> AgentState:
    """Write an email based on user input and return the email content."""
    
    llm_for_email = ChatOpenAI(
        model="prisma_gemini_pro",
        base_url="https://api-dev.ai.auth.axis.cloud/v1",
        api_key=os.getenv("AXIS_DEV_API_KEY"),
        max_tokens=300,
        temperature=0.7  
    )
    
    user_input = state["messages"][-1].content # comes from the agent state, which is the original user input
  
    # Simplified direct prompt
    email_prompt = f"""Write a professional and very concise email for the following request:{user_input}, and make sure the email is no more than 100 words. 
    Email:
    """
    
    # Directly invoke the LLM to get the email content, without tool calling
    response = llm_for_email.invoke([HumanMessage(content=email_prompt)])
    answer = response.content
    
    #print(f"Email Agent Result: {answer}")
    
    return {
        **state,
        "final_answer": answer
    }
