import os
import json
from file_utils import identify_file_types, get_pdf_files
from processing.pdf_processor import extract_text_from_pdf, extract_metadata
from processing.text_preprocessor import preprocess_text, chunk_text
from processing.copyright_filter import CopyrightDatabase, filter_copyrighted_content

def process_pdf(pdf_path, copyright_db):
    # Extract text
    text = extract_text_from_pdf(pdf_path)
    
    # Preprocess text
    processed_text = preprocess_text(text)
    
    # Chunk text
    chunked_text = chunk_text(processed_text)
    
    # Filter copyrighted content
    filtered_chunks = filter_copyrighted_content(chunked_text, copyright_db)
    
    # Extract metadata
    metadata = extract_metadata(pdf_path)
    
    # Combine chunks with metadata
    result = []
    for i, chunk in enumerate(filtered_chunks):
        result.append({
            'chunk_id': f"{metadata['title']}_{i}",
            'text': chunk,
            'metadata': metadata
        })
    
    return result

def process_pdf_directory(directory):
    copyright_db = CopyrightDatabase()
    
    # Identify file types
    file_types = identify_file_types(directory)
    print("File types in directory:", file_types)
    
    # Get PDF files
    pdf_files = get_pdf_files(directory)
    
    all_results = []
    for file in pdf_files:
        pdf_path = os.path.join(directory, file)
        print(f"Processing {file}...")
        all_results.extend(process_pdf(pdf_path, copyright_db))
    
    # Save results to a JSON file
    output_file = 'preprocessed_data.json'
    with open(output_file, 'w') as f:
        json.dump(all_results, f)
    
    print(f"Preprocessing complete. Results saved to {output_file}")

if __name__ == "__main__":
    directory = input("Enter the path to your dataset directory: ")
    process_pdf_directory(directory)