import os
from pathlib import Path

def identify_file_types(directory):
    file_types = {}
    for file in os.listdir(directory):
        file_path = Path(directory) / file
        file_type = file_path.suffix.lower()
        file_types[file_type] = file_types.get(file_type, 0) + 1
    return file_types

def get_pdf_files(directory):
    return [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]