import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import torch
from file_utils import identify_file_types, get_pdf_files
from processing.pdf_processor import extract_text_from_pdf, extract_metadata
from processing.text_preprocessor import preprocess_text, chunk_text
from processing.copyright_filter import CopyrightDatabase, filter_copyrighted_content

class DatasetProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Dataset Processor")
        master.geometry("400x250")

        # Initialize status_var here
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(master, textvariable=self.status_var)
        self.status_label.pack(pady=5)

        self.setup_directories()
        self.check_gpu()

        self.label = tk.Label(master, text="Select a directory containing PDF files:")
        self.label.pack(pady=10)

        self.select_button = tk.Button(master, text="Select Directory", command=self.select_directory)
        self.select_button.pack(pady=5)

        self.selected_path = tk.StringVar()
        self.path_label = tk.Label(master, textvariable=self.selected_path)
        self.path_label.pack(pady=5)

        self.start_button = tk.Button(master, text="Start Processing", command=self.start_processing, state=tk.DISABLED)
        self.start_button.pack(pady=10)

    def setup_directories(self):
        # only way I could get it to work without it saying "permission denied" but now it always creates a directory called /~/ in the root folder... 
        # idk how tf to fix this im probably just stupid
        
        self.finetuning_dir = "~/data/"
        self.processed_data_dir = os.path.join(self.finetuning_dir, "data", "preprocessed_data")

        try:
            os.makedirs(self.processed_data_dir, exist_ok=True)
        except PermissionError as e:
            messagebox.showerror("Error", f"Permission denied: {e}\nPlease run the script with appropriate permissions.")
            raise

    def check_gpu(self):
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            gpu_name = torch.cuda.get_device_name(0)
            self.status_var.set(f"GPU available: {gpu_name}")
        else:
            self.device = torch.device("cpu")
            self.status_var.set("No GPU available. Using CPU.")

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
            output_file = self.process_directory(input_path)
            self.status_var.set(f"Processing complete. Output saved to:\n{output_file}")
        except Exception as e:
            self.status_var.set(f"Error occurred: {str(e)}")
            messagebox.showerror("Error", str(e))
        print ("processing complete")
        
    def process_directory(self, directory):
        copyright_db = CopyrightDatabase()
        file_types = identify_file_types(directory)
        print("File types in directory:", file_types)
        pdf_files = get_pdf_files(directory)
        all_results = []

        for file in pdf_files:
            pdf_path = os.path.join(directory, file)
            print(f"Processing {file}...")
            try:
                # Process the PDF
                all_results.extend(self.process_pdf(pdf_path, copyright_db))
            except PermissionError as e:
                print(f"Permission error processing {file}: {e}")
            except Exception as e:
                print(f"Error processing {file}: {e}")

        # Save processed data as JSON in the processed_data directory
        output_file = os.path.join(self.processed_data_dir, 'preprocessed_data.json')
        try:
            with open(output_file, 'w') as f:
                json.dump(all_results, f)
        except PermissionError as e:
            raise PermissionError(f"Unable to write output file: {e}")

        return output_file

    def process_pdf(self, pdf_path, copyright_db):
        text = extract_text_from_pdf(pdf_path, self.device)
        processed_text = preprocess_text(text)
        chunked_text = chunk_text(processed_text)
        filtered_chunks = filter_copyrighted_content(chunked_text, copyright_db, self.device)
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
    try:
        app = DatasetProcessorGUI(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", str(e))
