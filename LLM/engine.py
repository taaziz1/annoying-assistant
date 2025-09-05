from LLM import agent_executor, sys_msg, HumanMessage
import re

def run_command(user_prompt: str) -> str:
    user_input = user_prompt.strip()
    human_msg = HumanMessage(content=user_input)

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
            # Only extract the final message from the AI agent, discard the thingking process
            # Overwrite with the latest AI message
            last_message = event['agent']['messages'][0].content

    response_text = None

    # If tool is called, print the message from tool
    if tool_called:
        response_text = tool_message
    # Check if AI agent generate a response
    elif last_message:
        # Remove the <think> .. </think> section of the AI response
        response_text = re.sub(r"<think>.*?</think>\s*", "", last_message, flags=re.DOTALL).strip()
    else:
        response_text = "Sorry, I couldn't produce a response."

    return response_text