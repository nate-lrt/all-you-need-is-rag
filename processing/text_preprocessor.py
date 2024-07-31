import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    sentences = sent_tokenize(text)
    stop_words = set(stopwords.words('english'))
    processed_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [word for word in words if word not in stop_words]
        processed_sentences.append(' '.join(words))
    return processed_sentences

def chunk_text(sentences, chunk_size=1000, overlap=200):
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence)
        
        if sentence_length > chunk_size:
            # Handle long sentences by splitting them
            words = sentence.split()
            while words:
                chunk = []
                chunk_length = 0
                while words and chunk_length + len(words[0]) + 1 <= chunk_size:
                    word = words.pop(0)
                    chunk.append(word)
                    chunk_length += len(word) + 1
                chunks.append(' '.join(chunk))
        elif current_length + sentence_length > chunk_size and current_chunk:
            # Start a new chunk
            chunks.append(' '.join(current_chunk))
            # Keep the overlap from the previous chunk
            overlap_words = ' '.join(current_chunk).split()[-overlap//10:]
            current_chunk = overlap_words
            current_length = sum(len(word) + 1 for word in overlap_words)
        
        current_chunk.append(sentence)
        current_length += sentence_length + 1  # +1 for space
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks
    