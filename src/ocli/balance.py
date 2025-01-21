from solana.rpc.api import Client
from solders.pubkey import Pubkey

# Initialize Solana Client
solana_client = Client("https://api.devnet.solana.com")  # Change to mainnet if needed

def check_balance(wallet_address: str) -> str:
    """
    Check the SOL balance of a given wallet address.
    
    Args:
        wallet_address (str): The wallet's public address in Base58 format.
        
    Returns:
        str: The balance of the wallet in SOL or an error message.
    """
    try:
        # Convert the address to a Pubkey
        pubkey = Pubkey.from_string(wallet_address)
        
        # Fetch the balance in lamports
        response = solana_client.get_balance(pubkey)
        if response.value is not None:
            balance_in_sol = response.value / 1e9  # Convert lamports to SOL
            return f"The wallet {wallet_address} has a balance of {balance_in_sol} SOL."
        else:
            return f"Failed to fetch balance for wallet: {wallet_address}. Error: {response.error.message}"
    except Exception as e:
        return f"Error checking balance: {str(e)}"

# Wrap as a FunctionTool


