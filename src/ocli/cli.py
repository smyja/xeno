import click
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
def main():
    """My CLI tool for doing awesome things."""
    pass

@main.command()
@click.option('--count', default=1, help='Number of times to greet.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def greet(count: int, name: str):
    """Greet someone multiple times."""
    for _ in range(count):
        console.print(f"Hello, [bold green]{name}[/bold green]! 👋")

@main.command()
def list_items():
    """Display a fancy table of items."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Description")

    # Add some sample data
    table.add_row("1", "Item A", "Description for item A")
    table.add_row("2", "Item B", "Description for item B")
    table.add_row("3", "Item C", "Description for item C")

    console.print(table)

if __name__ == '__main__':
    main()