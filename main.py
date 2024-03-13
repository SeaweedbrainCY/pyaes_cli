import typer
import os
from rich import print
from typing_extensions import Annotated
from rich.progress import Progress, SpinnerColumn, TextColumn
import time
import src.compression as compression

app = typer.Typer()


@app.command()
def enc(file_path: str, password: Annotated[
        str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)
    ],):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        if not os.path.exists(file_path):
            print(f"[bold red]File {file_path} not found[/bold red]")
            raise typer.Abort()
        progress.add_task(description="Compressing...", total=None)
        compression.compress(file_path)

        

@app.command()
def dec(file_path: str):
    print(f"Decrypting {file_path}")


if __name__ == "__main__":
    app()
