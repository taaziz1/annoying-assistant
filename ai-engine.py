from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool


@tool
def check_working() -> str:
    """Useful for when user want to check if the tool function is working"""
    return 'Tool is working!!!'

model = ChatOllama(model="qwen3:8b", temperature=0.7)

tools = [check_working]

agent_executor = create_react_agent(model, tools)

sys_msg = SystemMessage(content=("You have a tool called check_working()"
                                 "When user want to check if tool is working, you must call the check_working() tool."
                                 "If there is no tool to be called, you can answer the question."))

print("User: ", end="")
user_input = input().strip()
human_msg = HumanMessage(content=user_input)

for event in agent_executor.stream({"messages": [sys_msg, human_msg]}):
    if "tools" in event:
        print(event['tools']['messages'][0].content)
    else:
        for _, payload in event.items():
            for msg in payload['messages']:
                print(msg)

