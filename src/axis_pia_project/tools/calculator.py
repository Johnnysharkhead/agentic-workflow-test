from langchain_core.tools import tool

# define the calulate function and wrap it as a tool (bind to the Calculator Agent later)
# Using langchain's tool decorator to wrap the function, which allows the agent to call it as a tool when needed
@tool
def dummy_calculator(expression: str) -> str:
    """
    This a simple calculator function that evaluates basic math expressions.
    
    Input: A string containing a math expression (e.g., "2 + 4 * 4")
    
    Output: The result of the expression as a string (e.g., "18")
    
    """
    try:
        result = eval(expression)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error: {str(e)}"
