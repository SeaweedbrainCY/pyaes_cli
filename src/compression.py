import pathlib
import zipfile
import typer
from uuid import uuid4

def compress(file_path:str):
    zip_file_path = f"/tmp/{uuid4()}.zip"
    file_path = pathlib.Path(file_path)
    if file_path.is_dir():
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for file in file_path.rglob('*'):
                zipf.write(file, file.relative_to(file_path))
    else:
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            zipf.write(file_path)
    
    return zip_file_path