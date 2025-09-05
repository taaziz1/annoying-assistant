from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from LLM.tools import open_app, close_app, go_to_url, google_search

model = ChatOllama(model="qwen3:8b", reasoning=False, top_p=0.8, temperature=0.7, top_k=20, min_p=0)

tools = [open_app, close_app, go_to_url, google_search]

agent_executor = create_react_agent(model, tools)

sys_msg = SystemMessage(content=("You have tools: open_app, close_app"
                                 "When the user asks to open/close apps, go to a website, google_search you MUST call the appropriate tool."
                                 "If there is no tool to be called, you can answer the question."
                                 "If user type in chrome, you should interpret it as Google Chrome."
                                 "If user type in edge, you should interpret it as Microsoft Edge"
                                 "When you cannot answer something without access to the Internet, call the tool google_search and paste the user's question into that function")
                        )