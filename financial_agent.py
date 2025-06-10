#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
financial_agent.py

A conversational financial analysis tool using agno agents for web search and financial data.
"""

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv
import re
import traceback


load_dotenv()
MODEL = "deepseek-r1-distill-llama-70b"

# web search agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for information",
    model=Groq(id=MODEL),
    tools=[DuckDuckGoTools()],
    instructions=["Always include the source of the information in your response"],
    show_tool_calls=True,
    markdown=True,
)


# financial agent
financial_agent = Agent(
    name="Financial Agent",
    role="Analyze financial data",
    model=Groq(id=MODEL),
    tools=[YFinanceTools(
        stock_price=True, company_info=True, stock_fundamentals=True, income_statements=True,
        key_financial_ratios=True, analyst_recommendations=True, technical_indicators=True, historical_prices=True
    )],
    instructions=["Use tables to display the data"],
    show_tool_calls=True,
    markdown=True,
)


multi_ai_agent = Agent(
    team=[web_search_agent, financial_agent],
    model=Groq(id=MODEL),
    instructions=[
        "You are a financial analyst. You are given a question and you need to answer it based on the information provided by the web search agent and the financial agent.",
        "Always include the source of the information in your response",
        "Use tables to display the data"
    ],
    show_tool_calls=True,
    markdown=True,
)

class ConversationManager:
    def __init__(self, agent):
        self.agent = agent
        self.conversation_history = []
        self.current_context = {}

    def add_to_history(self, role, content):
        if content is not None:
            self.conversation_history.append({"role": role, "content": str(content)})

    def get_context(self):
        recent_messages = [
            f"{msg['role']}: {msg['content']}"
            for msg in self.conversation_history[-4:]
            if msg['content'] is not None
        ]
        return "\n".join(recent_messages)

    def process_query(self, user_input, stream=True):
        self.add_to_history("user", user_input)
        if len(self.conversation_history) > 1:
            company_context = self._extract_company_context(user_input)
            context = f"""Previous conversation context:
- Currently discussing: {company_context}
- Recent messages:
{self.get_context()}

Based on this context, please answer: {user_input}"""
        else:
            context = user_input

        try:
            response = self.agent.print_response(context, stream=stream)
            if response:
                self.add_to_history("assistant", str(response))
            return response
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            traceback.print_exc()
            return None

    def _extract_company_context(self, user_input):
        # Try to extract a stock symbol (e.g., TATAMOTORS.NS) or company name from user input
        match = re.search(r'([A-Z]{2,}\.[A-Z]{2,})', user_input)
        if match:
            self.current_context["company"] = match.group(1)
        else:
            # Fallback: look for a capitalized word (company name)
            match = re.search(r'\b([A-Z][a-zA-Z]+)\b', user_input)
            if match:
                self.current_context["company"] = match.group(1)
        return self.current_context.get("company", "No specific company")

def main():
    conversation = ConversationManager(multi_ai_agent)
    while True:
        try:
            user_input = input("\nEnter your question (or 'quit' to exit): ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            conversation.process_query(user_input)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            traceback.print_exc()

if __name__ == "__main__":
    main()
