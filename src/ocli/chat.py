import os
from dotenv import load_dotenv
load_dotenv()
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.core import Settings
from llama_index.tools.yahoo_finance import YahooFinanceToolSpec
from llama_index.llms.openrouter import OpenRouter
from wallet import generate_solana_wallet
# from transact import execute_solana_transaction
# settings
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.storage.chat_store import SimpleChatStore
# Initialize a simple chat store

Settings.llm = OpenRouter(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    max_tokens=5000,
    context_window=200000,
    model="google/gemini-pro-1.5"
)
# Load the chat store from a file
loaded_chat_store = SimpleChatStore.from_persist_path(
    persist_path="chat_store.json"
)
# Create a memory buffer with the loaded chat store
memory = ChatMemoryBuffer.from_defaults(
    token_limit=6000, 
    chat_store=loaded_chat_store, 
    chat_store_key="session1"
)
# Wrap the wallet generation function
generate_wallet_tool = FunctionTool.from_defaults(fn=generate_solana_wallet)
# Create the agent with the tools, memory, and LLM
agent = ReActAgent.from_tools([generate_wallet_tool], memory=memory,verbose=True)
# Interact with the agent
response = agent.chat("previous wallet address?")
print(response)
# Persist the updated chat history
loaded_chat_store.persist("chat_store.json")