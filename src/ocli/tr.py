import os
import time
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solana.rpc.api import Client
from llama_index.core.tools import FunctionTool

# Load environment variables
load_dotenv()
private_key = os.getenv("PRIVATE_KEY")
main_wallet = os.getenv("MAIN_WALLET")

def execute_transaction(recipient_wallet: str, amount: float) -> str:
    """
    Execute a Solana transaction from the main wallet to a recipient's wallet.
    
    Args:
        recipient_wallet (str): Public key of the recipient's wallet.
        amount (float): Amount in SOL to transfer.
        
    Returns:
        str: Transaction result message or error.
    """
    try:
        if not private_key or not main_wallet:
            return "Missing configuration in .env. Ensure PRIVATE_KEY and MAIN_WALLET are set."

        # Initialize the client
        solana_client = Client("https://api.devnet.solana.com")
        
        # Convert private key string to bytes and create sender's keypair
        private_key_bytes = bytes.fromhex(private_key)
        sender_keypair = Keypair.from_bytes(private_key_bytes)
        
        # Set up public keys
        sender_pubkey = Pubkey.from_string(main_wallet)
        recipient_pubkey = Pubkey.from_string(recipient_wallet)
        
        # Check sender's balance
        initial_balance = float(solana_client.get_balance(sender_pubkey).value) / 1e9
        print(f"Initial balance: {initial_balance} SOL")
        
        # Ensure sufficient balance (including fees)
        required_amount = amount + 0.000005  # Adding estimated transaction fee
        if initial_balance < required_amount:
            return f"Insufficient balance. Have {initial_balance} SOL, need {required_amount} SOL (including fees)"
        
        # Get latest blockhash
        latest_blockhash_info = solana_client.get_latest_blockhash()
        recent_blockhash = latest_blockhash_info.value.blockhash
        print(f"Got blockhash: {recent_blockhash}")
        
        # Create transfer instruction
        transfer_instruction = transfer(TransferParams(
            from_pubkey=sender_pubkey,
            to_pubkey=recipient_pubkey,
            lamports=int(amount * 1e9)  # Convert SOL to lamports
        ))
        
        # Create transaction
        transaction = Transaction.new_signed_with_payer(
            [transfer_instruction],  # instructions
            sender_pubkey,           # payer
            [sender_keypair],        # signers
            recent_blockhash         # recent_blockhash
        )
        
        print("Transaction created successfully")
        
        # Send transaction
        result = solana_client.send_transaction(transaction)
        transaction_signature = result.value
        print(f"Transaction Signature: {transaction_signature}")
        
        # Check transaction status
        success, status_or_error = check_transaction_status(solana_client, transaction_signature)
        
        if success:
            print(f"\nTransaction {status_or_error}!")
            # Wait for balance to update and return new balance
            time.sleep(3)
            new_balance = float(solana_client.get_balance(sender_pubkey).value) / 1e9
            return (
                f"Transaction confirmed! Transferred {amount} SOL to {recipient_wallet}. "
                f"New balance: {new_balance} SOL."
            )
        else:
            return f"Transaction failed: {status_or_error}"
    
    except Exception as e:
        return f"Transaction error: {str(e)}"


def check_transaction_status(client: Client, signature: str, max_retries: int = 60, retry_delay: float = 1.0):
    """Check transaction status with detailed error handling and longer timeout."""
    print("\nChecking transaction status...")
    for i in range(max_retries):
        try:
            # Check if transaction is finalized
            response = client.get_signature_statuses([signature])
            if response.value[0] is not None:
                status = str(response.value[0].confirmation_status)
                print(f"Current status: {status}")
                if "confirmed" in status.lower() or "finalized" in status.lower():
                    return True, status
        except Exception as e:
            print(f"Error checking status (attempt {i+1}/{max_retries}): {str(e)}")
        time.sleep(retry_delay)
    return False, "Transaction confirmation timed out"



