# OCLI

OCLI is a command-line interface (CLI) tool designed to perform various tasks, including interacting with Solana wallets, sending emails, and more. This tool leverages the power of Python and several libraries to provide a seamless experience.

## Features

- Interactive chat session with Claudia, an AI agent.
- Solana wallet management and transactions.
- Email sending via Zoho's SMTP server.
- Web scraping capabilities.

## Requirements

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ocli.git
   cd ocli   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt   ```

4. **Install the package:**
   ```bash
   pip install .   ```

## Configuration

1. **Environment Variables:**

   Create a `.env` file in the root directory and add the following variables:
   ```plaintext
   OPENROUTER_API_KEY=your_openrouter_api_key
   ZOHO_EMAIL=your_zoho_email
   ZOHO_PASSWORD=your_zoho_password
   PRIVATE_KEY=your_private_key
   MAIN_WALLET=your_main_wallet_address   ```

## Usage

- **Start the CLI:**

  To start the CLI, run the following command:
  ```bash
  ocli  ```

- **Chat with Claudia:**

  To start an interactive chat session, use the following command:
  ```bash
  ocli chat  ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
