from solana_simplified import Solana_Simplified
import time

# Configuration
private_key = "<sender_account_private_key>"
main_wallet = "<sender_account_wallet_address>"
test_wallet = "<recipient_account_wallet_address>"
program_id = "<token_program_id>"  # Example: TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
mint = "<token_address>"  # Example: FpekncBMe3Vsi1LMkh6zbNq8pdM6xEbNiFsJBRcPbMDQ

# Set up wallet keypair and clients
source_main_wallet_keypair = Solana_Simplified.set_source_main_wallet_keypair(private_key)
sender_pubkey = Solana_Simplified.set_main_wallet_publickey(main_wallet)
destination_pubkey = Solana_Simplified.set_main_wallet_publickey(test_wallet)
program_pubkey = Solana_Simplified.set_program_id_publickey(program_id)
token_address_pubkey = Solana_Simplified.set_token_address_publickey(mint)

solana_client = Solana_Simplified.set_solana_client()
spl_client = Solana_Simplified.set_spl_client(solana_client, token_address_pubkey, program_pubkey, source_main_wallet_keypair)

# Check wallet balances
def check_wallet_balances():
    sender_solana_balance = Solana_Simplified.get_main_wallet_solana_balance(solana_client, sender_pubkey)
    sender_token_balance = Solana_Simplified.get_token_account_balance(spl_client, 
                                 Solana_Simplified.get_token_wallet_address_from_main_wallet_address(spl_client, sender_pubkey))
    
    destination_solana_balance = Solana_Simplified.get_main_wallet_solana_balance(solana_client, destination_pubkey)
    destination_token_balance = Solana_Simplified.get_token_account_balance(spl_client, 
                                    Solana_Simplified.get_token_wallet_address_from_main_wallet_address(spl_client, destination_pubkey))
    
    print(f"Sender SOL Balance: {sender_solana_balance} SOL")
    print(f"Sender Token Balance: {sender_token_balance} Tokens")
    print(f"Recipient SOL Balance: {destination_solana_balance} SOL")
    print(f"Recipient Token Balance: {destination_token_balance} Tokens")

# Transfer tokens
def transfer_tokens(amount: int):
    sender_token_pubkey = Solana_Simplified.get_token_wallet_address_from_main_wallet_address(spl_client, sender_pubkey)
    destination_token_pubkey = Solana_Simplified.get_token_wallet_address_from_main_wallet_address(spl_client, destination_pubkey)

    transaction = Solana_Simplified.send_spl_token(spl_client, sender_token_pubkey, destination_token_pubkey, source_main_wallet_keypair, amount)
    signature = Solana_Simplified.set_transaction_signature(transaction)

    time.sleep(20)  # Wait for transaction confirmation
    status = Solana_Simplified.check_token_transaction(solana_client, signature)

    print(f"Token Transfer Transaction Signature: {signature}")
    print(f"Transaction Status: {status}")

# Transfer SOL
def transfer_sol(amount: float):
    transaction = Solana_Simplified.send_solana(solana_client, sender_pubkey, destination_pubkey, source_main_wallet_keypair, amount)
    signature = Solana_Simplified.set_transaction_signature(transaction)

    time.sleep(20)  # Wait for transaction confirmation
    status = Solana_Simplified.check_solana_transaction(solana_client, signature)

    print(f"SOL Transfer Transaction Signature: {signature}")
    print(f"Transaction Status: {status}")

# Main execution
if __name__ == "__main__":
    # Check balances before transfer
    print("Checking wallet balances before transfer:")
    check_wallet_balances()

    # Transfer tokens (1 token as an example)
    # print("\nTransferring 1 token...")
    # transfer_tokens(1)

    # # Transfer SOL (0.001 SOL as an example)
    # print("\nTransferring 0.001 SOL...")
    # transfer_sol(0.001)

    # # Check balances after transfer
    # print("\nChecking wallet balances after transfer:")
    # check_wallet_balances()
