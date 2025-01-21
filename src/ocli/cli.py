
# cli.py
import click
from rich.console import Console
from rich.prompt import Prompt
from .chat import ChatManager

console = Console()

@click.group()
def main():
    """My CLI tool for doing awesome things."""
    pass

@main.command()
def chat():
    """Start an interactive chat session with Claudia."""
    chat_manager = ChatManager()
    console.print("[bold green]Welcome to the chat! Type 'exit' to quit.[/bold green]")
    
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("[bold blue]You[/bold blue]")
            
            # Exit condition
            if user_input.lower() in {'exit', 'quit', 'q'}:
                console.print("[bold red]Goodbye![/bold red]")
                break
            
            # Get response and automatically persist
            response = chat_manager.chat(user_input)
            console.print(f"[bold yellow]Claudia:[/bold yellow] {response}")
            
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")

if __name__ == '__main__':
    main()