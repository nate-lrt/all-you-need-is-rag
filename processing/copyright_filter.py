from fuzzywuzzy import fuzz

class CopyrightDatabase:
    def __init__(self):
        # This is a placeholder. In a real scenario, you'd load actual copyright data.
        self.copyrighted_texts = [
            "This is a sample copyrighted text.",
            "Another example of protected content."
        ]

    def has_exact_match(self, text):
        return text in self.copyrighted_texts

    def get_all_texts(self):
        return self.copyrighted_texts

def is_potentially_copyrighted(chunk, copyright_db, device):
    # The device parameter is not used here, but included for consistency
    if copyright_db.has_exact_match(chunk):
        return True
    
    for copyrighted_text in copyright_db.get_all_texts():
        if fuzz.ratio(chunk, copyrighted_text) > 80:  # Adjust threshold as needed
            return True
    
    return False

def filter_copyrighted_content(chunks, copyright_db, device):
    return [chunk for chunk in chunks if not is_potentially_copyrighted(chunk, copyright_db, device)]