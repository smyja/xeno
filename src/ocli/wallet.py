import json
from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
from solders.keypair import Keypair

def generate_solana_wallet():
    """For creating a new wallet if there's no previous wallet'."""
    # Generate mnemonic
    mnemo = Mnemonic("english")
    mnemonic_phrase = mnemo.generate(strength=256)

    # Generate seed
    seed_bytes = Bip39SeedGenerator(mnemonic_phrase).Generate()

    # Use Phantom's derivation path
    bip44_sol = (Bip44.FromSeed(seed_bytes, Bip44Coins.SOLANA)
                 .Purpose()
                 .Coin()
                 .Account(0)
                 .Change(Bip44Changes.CHAIN_EXT)
                 .AddressIndex(0))

    derived_private_key = bip44_sol.PrivateKey().Raw().ToBytes()
    keypair = Keypair.from_seed(derived_private_key)

    wallet_data = {
        "mnemonic": mnemonic_phrase,
        "public_key": str(keypair.pubkey()),
        "secret_key": bytes(keypair).hex()
    }

    with open("olsolana_wallet.json", "w") as f:
        json.dump(wallet_data, f, indent=4)

    return {
        "message": "✅ Wallet successfully saved to solana_wallet.json",
        "mnemonic_phrase": mnemonic_phrase,
        "address": str(keypair.pubkey())
    }
