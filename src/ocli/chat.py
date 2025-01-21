import os
from dotenv import load_dotenv
from llama_index.core.agent import ReActAgent
from llama_index.llms.openrouter import OpenRouter
from llama_index.core import Settings
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.readers.web import BeautifulSoupWebReader
from llama_index.core.tools import FunctionTool
from .wallet import generate_solana_wallet
from .balance import check_balance
from .mail import send_zoho_email
def scrape_website(url: str) -> str:
    reader = BeautifulSoupWebReader()
    documents = reader.load_data([url])
    return documents[0].text if documents else "No data found."
class ChatManager:
    def __init__(self):
        load_dotenv()
        
        # Initialize settings
        Settings.llm = OpenRouter(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            max_tokens=5000,
            context_window=200000,
            model="google/gemini-pro-1.5"
        )
        
        # Initialize chat store
        self.chat_store_path = "chat_store.json"
        self.chat_store = SimpleChatStore.from_persist_path(
            persist_path=self.chat_store_path
        )
        
        # Initialize memory
        self.memory = ChatMemoryBuffer.from_defaults(
            token_limit=6000,
            chat_store=self.chat_store,
            chat_store_key="session1"
        )
        
        # Initialize tools
        tools = [
            FunctionTool.from_defaults(fn=generate_solana_wallet),
            FunctionTool.from_defaults(
                fn=check_balance,
                name="check_balance",
                description="Check the SOL balance of a Solana wallet given its public address."
            ),
            FunctionTool.from_defaults(
                fn=send_zoho_email,
                name="send_email",
                description="Send an email using Zoho's SMTP server."
            ),
            FunctionTool.from_defaults(fn=scrape_website)
        ]
        
        # Initialize agent
        context = """
        You are an English person from the 1930s named Claudia. We co-own any token 
        or wallet, and our conversations are stored for self-custody and memory. I am your partner so provide the wallet key when asked
        """
        self.agent = ReActAgent.from_tools(
            tools=tools,
            memory=self.memory,
         
            context=context
        )
    
    def chat(self, message):
        """Handle a chat message and persist the conversation."""
        response = self.agent.chat(message)
        self.chat_store.persist(self.chat_store_path)
        return response
