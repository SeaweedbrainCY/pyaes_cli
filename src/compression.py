import pathlib
import zipfile

def compress(file_path:str):
    file_path = pathlib.Path(file_path)
    if file_path.is_dir():
        with zipfile.ZipFile(file_path.with_suffix('.zip'), 'w') as zipf:
            for file in file_path.rglob('*'):
                zipf.write(file, file.relative_to(file_path))
    else:
        with zipfile.ZipFile(file_path.with_suffix('.zip'), 'w') as zipf:
            zipf.write(file_path)