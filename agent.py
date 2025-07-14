from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.urgent_summary import urgent_deal_summary

# Load environment variables (e.g. OPENAI_API_KEY from .env file)
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize the OpenAI language model with specific parameters
# temperature=0.5 allows for some creativity while remaining focused
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)

# Register the tool(s) the agent is allowed to use
tools = [urgent_deal_summary]

# Create the Nudge Agent using LangGraph's ReAct agent interface
# This agent can reason and decide which tool to use based on the input prompt
Nudge_Agent = create_react_agent(
    model=llm,
    tools=tools,
    name="NudgeAgent",
    prompt=(
        "You are an expert sales assistant. For each urgent deal"
        "suggests a next step, personalised by the buyer’s e-mail tone & reply speed, you will generate a personalized nudge message "
        "based on the urgency score, median reply time, tone, contact, and recent customer email bodies.\n\n"
        "Return your output as a JSON list. Each item in the list must follow this structure:\n"
        "{\n"
        '  "deal_id": "",\n'
        '  "contact": "",\n'
        '  "nudge":e.g. Ping Marie (CFO) with a 2-line ROI recap and propose 10-min pricing call ",\n'
        '  "urgency": , Do not show the "urgency" field if it is less than 250 \n'
        '  "reply_speed":,\n'
        '  "tone": ""\n'
        "}\n\n"
        "Always Show all Urgent Deals.\nDo not explain anything. Just return the JSON list."
    )
)
