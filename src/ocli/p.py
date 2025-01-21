from solana.rpc.api import Client
from solders.pubkey import Pubkey  # Import Pubkey class

def check_wallet_balance(wallet_address):
    """
    Check the balance of a given Solana wallet address.
    """
    # Connect to Solana RPC (testnet or mainnet URL can be used)
    client = Client("https://api.devnet.solana.com")  # Change to mainnet if required

    try:
        # Decode base58 address to Pubkey
        public_key = Pubkey.from_string(wallet_address)

        # Fetch the wallet balance
        response = client.get_balance(public_key)
        
        # Access the balance value directly from the response object
        lamports = response.value  # Get balance in lamports
        sol = lamports / 1e9  # Convert lamports to SOL
        return f"{wallet_address}: {sol} SOL"

    except Exception as e:
        return f"Error processing wallet address {wallet_address}: {str(e)}"

# Addresses to check
wallet_addresses = [
    "FA1rQHH4BLtFyh9uRfbsVkhwcvKY1Bb9habT1FpxJxuQ",
    "AtcGKwhAD7QAj7WdeGMvAJJYhwEBuLVdPCZqvpQU9JbM"
]

# Check balances for each wallet
for address in wallet_addresses:
    print(check_wallet_balance(address))
