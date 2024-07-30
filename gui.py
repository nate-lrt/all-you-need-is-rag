import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import shutil
from file_utils import identify_file_types, get_pdf_files
from processing.pdf_processor import extract_text_from_pdf, extract_metadata
from processing.text_preprocessor import preprocess_text, chunk_text
from processing.copyright_filter import CopyrightDatabase, filter_copyrighted_content

class DatasetProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Dataset Processor")
        master.geometry("400x200")

        self.label = tk.Label(master, text="Select a directory containing PDF files:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Select Directory", command=self.select_directory)
        self.select_button.pack(pady=5)

        self.selected_path = tk.StringVar()
        self.path_label = tk.Label(master, textvariable=self.selected_path)
        self.path_label.pack(pady=5)

        self.start_button = tk.Button(master, text="Start Processing", command=self.start_processing, state=tk.DISABLED)
        self.start_button.pack(pady=10)

        self.status_var = tk.StringVar()
        self.status_label = tk.Label(master, textvariable=self.status_var)
        self.status_label.pack(pady=5)

    def select_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.selected_path.set(path)
            self.start_button['state'] = tk.NORMAL

    def start_processing(self):
        input_path = self.selected_path.get()
        if not input_path:
            messagebox.showerror("Error", "Please select a directory first.")
            return

        self.status_var.set("Processing...")
        self.master.update()

        try:
            output_dir = self.process_directory(input_path)
            self.status_var.set(f"Processing complete. Output saved to:\n{output_dir}")
        except Exception as e:
            self.status_var.set(f"Error occurred: {str(e)}")

    def process_directory(self, directory):
        copyright_db = CopyrightDatabase()
        
        file_types = identify_file_types(directory)
        print("File types in directory:", file_types)
        
        pdf_files = get_pdf_files(directory)
        
        # Create the output directory structure
        output_base_dir = "/finetuning/data"
        raw_data_dir = os.path.join(output_base_dir, "raw_data")
        processed_data_dir = os.path.join(output_base_dir, "preprocessed_data")
        
        os.makedirs(raw_data_dir, exist_ok=True)
        os.makedirs(processed_data_dir, exist_ok=True)

        all_results = []
        for file in pdf_files:
            pdf_path = os.path.join(directory, file)
            print(f"Processing {file}...")
            
            # Copy raw PDF to raw_data directory
            raw_pdf_path = os.path.join(raw_data_dir, file)
            shutil.copy2(pdf_path, raw_pdf_path)
            
            # Process the PDF
            processed_data = self.process_pdf(pdf_path, copyright_db)
            all_results.extend(processed_data)
        
        # Save processed data as JSON
        output_file = os.path.join(processed_data_dir, 'preprocessed_data.json')
        with open(output_file, 'w') as f:
            json.dump(all_results, f)
        
        return output_base_dir

    def process_pdf(self, pdf_path, copyright_db):
        text = extract_text_from_pdf(pdf_path)
        processed_text = preprocess_text(text)
        chunked_text = chunk_text(processed_text)
        filtered_chunks = filter_copyrighted_content(chunked_text, copyright_db)
        metadata = extract_metadata(pdf_path)
        
        result = []
        for i, chunk in enumerate(filtered_chunks):
            result.append({
                'chunk_id': f"{metadata['title']}_{i}",
                'text': chunk,
                'metadata': metadata
            })
        
        return result

if __name__ == "__main__":
    root = tk.Tk()
    app = DatasetProcessorGUI(root)
    root.mainloop()