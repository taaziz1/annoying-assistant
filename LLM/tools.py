from langchain.tools import tool

@tool
def check_working() -> str:
    """Useful for when user want to check if the tool function is working"""
    return 'Tool is working!!!'