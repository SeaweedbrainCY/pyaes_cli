import typer
import os
from rich import print
from typing_extensions import Annotated
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
import time
import src.compression as compression
import src.derivation as derivation
import src.encryption as encryption
import pathlib


app = typer.Typer()


@app.command()
def enc(file_path: str, dest_path:str,password: Annotated[
        str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)
    ],):
        if not os.path.exists(file_path):
            print(f"[bold red]File {file_path} not found[/bold red]")
            raise typer.Abort()
        if file_path == dest_path:
            print(f"[bold red]Source and destination cannot be the same[/bold red]")
            raise typer.Abort()
        dest = pathlib.Path(dest_path)
        if dest.exists():
            delete = typer.confirm(f"\n{dest_path} already exists. Do you want to overwrite it?")
            if not delete:
                raise typer.Abort()
        with Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),transient=True,) as progress:
            progress.add_task(description="Compressing...", total=None)
            compressed_file_path = compression.compress(file_path)
            print("\n📦 [green]Compressed[/green]")
            progress.add_task(description="Deriving your key...", total=None)
            derived_key,key_salt = derivation.derive_key(password)
            print("🔑 [green]Key derived[/green]")
            progress.add_task(description="Encrypting...", total=None)
            encryption.encrypt(compressed_file_path, dest_path, derived_key, key_salt)
            os.remove(compressed_file_path)
            print(f"🔒 [green]{file_path} encrypted to {dest_path}[/green]")

        

        

        

@app.command()
def dec(file_path: str,dest_path:str, password: Annotated[
        str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)
    ],):
        if not os.path.exists(file_path):
            print(f"[bold red]File {file_path} not found[/bold red]")
            raise typer.Abort()
        if file_path == dest_path:
            print(f"[bold red]Source and destination cannot be the same[/bold red]")
            raise typer.Abort()
        dest = pathlib.Path(dest_path)
        if dest.exists():
            delete = typer.confirm(f"\n{dest_path} already exists. Do you want to overwrite it?")
            if not delete:
                raise typer.Abort()
        with Progress(SpinnerColumn(),TextColumn("[progress.description]{task.description}"),transient=True,) as progress:
            progress.add_task(description="Deriving your key...", total=None)
            derived_key,_ = derivation.derive_key(password, encryption.get_key_salt(file_path))
            print("\n🔑 [green]Key derived[/green]")
            progress.add_task(description="Decrypting...", total=None)
            decrypted_path = encryption.decrypt(file_path, derived_key)
            if not decrypted_path:
                print(f"[bold red]Invalid password[/bold red]")
                raise typer.Abort()
            print("🔓 [green]Decrypted[/green]")
            progress.add_task(description="Extracting...", total=None)
            compression.decompress(decrypted_path, dest_path)
            os.remove(decrypted_path)
            print(f"📦 [green]{file_path} decrypted to {dest_path}[/green]")



if __name__ == "__main__":
    app()
