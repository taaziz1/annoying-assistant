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

last_message = None
tool_called = False
tool_message = None
for event in agent_executor.stream({"messages": [sys_msg, human_msg]}):
    # Check to see if tool is called
    if "tools" in event:
        tool_called = True
        # Store the message from the tool
        tool_message = event['tools']['messages'][0].content
    else:
        for _, payload in event.items():
            # Take the messages from the AI agent, if no answer generated, return empty list
            for msg in payload.get('messages',[]):
                # Only extract the final message from the AI agent, discard the thingking process
                last_message = msg.content
# If tool is called, print the message from tool
if tool_called:
    print(tool_message)
# Check if AI agent generate a response
elif last_message:
    print(last_message)
else:
    print("Sorry, I couldn't produce a response.")

