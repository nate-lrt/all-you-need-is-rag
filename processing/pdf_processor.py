import PyPDF2
import torch

def extract_text_from_pdf(pdf_path, device):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    
    # Convert text to tensor and move to device
    text_tensor = torch.tensor([ord(c) for c in text], dtype=torch.long, device=device)
    # You can perform any GPU-accelerated operations here if needed
    # For now, we'll just convert it back to string
    return ''.join([chr(i) for i in text_tensor.cpu().numpy()])

def extract_metadata(pdf_path):
    # This function doesn't require GPU acceleration
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        metadata = reader.metadata
    return {
        'title': metadata.get('/Title', ''),
        'author': metadata.get('/Author', ''),
        'subject': metadata.get('/Subject', ''),
        'keywords': metadata.get('/Keywords', '')
    }