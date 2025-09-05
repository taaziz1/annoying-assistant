from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from LLM.tools import check_working

model = ChatOllama(model="qwen3:8b", reasoning=False, top_p=0.8, temperature=0.7, top_k=20, min_p=0)

tools = [check_working]

agent_executor = create_react_agent(model, tools)

sys_msg = SystemMessage(content=("You have a tool called check_working()"
                                 "When user want to check if tool is working, you must call the check_working() tool."
                                 "If there is no tool to be called, you can answer the question."))