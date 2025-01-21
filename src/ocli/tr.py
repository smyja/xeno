from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.message import Message
from solders.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solana.rpc.api import Client
import time

# Configuration
private_key = "6fa51980cf584633812c58d9035c799bca91e2e1980043a283c1d475369e3a83d252ceacde5801f0f70f142e6682a0e402fac8606e3efc200510a128ecafcb93"
main_wallet = "FA1rQHH4BLtFyh9uRfbsVkhwcvKY1Bb9habT1FpxJxuQ"
recipient_wallet = "AtcGKwhAD7QAj7WdeGMvAJJYhwEBuLVdPCZqvpQU9JbM"

def check_transaction_status(client: Client, signature: str, max_retries: int = 60, retry_delay: float = 1.0):
    """Check transaction status with detailed error handling and longer timeout."""
    print("\nChecking transaction status...")
    
    for i in range(max_retries):
        try:
            # First check if transaction is finalized
            response = client.get_signature_statuses([signature])
            if response.value[0] is not None:
                status = str(response.value[0].confirmation_status)
                print(f"Current status: {status}")
                
                # Convert status string to lowercase for comparison
                status_lower = status.lower()
                if "confirmed" in status_lower or "finalized" in status_lower:
                    return True, status
            
            # If not finalized, check if it failed
            tx_details = client.get_transaction(signature)
            if tx_details.value is not None:
                if hasattr(tx_details.value, 'err') and tx_details.value.err is not None:
                    return False, f"Transaction failed: {tx_details.value.err}"
            
        except Exception as e:
            print(f"Error checking status (attempt {i+1}/{max_retries}): {str(e)}")
        
        print(".", end="", flush=True)
        time.sleep(retry_delay)
    
    return False, "Transaction confirmation timed out"

def main():
    try:
        # Initialize the client
        solana_client = Client("https://api.devnet.solana.com")
        
        # Convert private key string to bytes and create keypair
        private_key_bytes = bytes.fromhex(private_key)
        sender_keypair = Keypair.from_bytes(private_key_bytes)
        
        # Set up public keys
        sender_pubkey = Pubkey.from_string(main_wallet)
        recipient_pubkey = Pubkey.from_string(recipient_wallet)
        
        # Check sender's balance
        initial_balance = float(solana_client.get_balance(sender_pubkey).value) / 1e9
        print(f"Initial balance: {initial_balance} SOL")
        
        # Ensure sufficient balance (including fees)
        amount = 0.1  # Amount to transfer
        required_amount = amount + 0.000005  # Adding estimated transaction fee
        if initial_balance < required_amount:
            raise ValueError(f"Insufficient balance. Have {initial_balance} SOL, need {required_amount} SOL (including fees)")
        
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
        
        # Check transaction status with improved handling
        print("Waiting for confirmation...", end="", flush=True)
        success, status_or_error = check_transaction_status(solana_client, transaction_signature)
        
        if success:
            print(f"\nTransaction {status_or_error}!")
            # Check new balance with retry
            for _ in range(3):  # Retry balance check a few times
                try:
                    time.sleep(1)  # Wait a bit for balance to update
                    new_balance = float(solana_client.get_balance(sender_pubkey).value) / 1e9
                    print(f"New balance: {new_balance} SOL")
                    if new_balance != initial_balance:
                        print(f"Amount transferred: {initial_balance - new_balance:.9f} SOL (including fee)")
                    break
                except Exception as e:
                    print(f"Error checking new balance: {e}")
                    time.sleep(1)
        else:
            print(f"\n{status_or_error}")
            
    except ValueError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"Error during transaction: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()