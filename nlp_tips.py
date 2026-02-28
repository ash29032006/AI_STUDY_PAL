import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import ssl

def setup_nltk():
    """Download required NLTK data on startup."""
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
        
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)

# Auto-download
setup_nltk()

def extract_keywords(text, top_n=5):
    """
    Tokenizes text, removes stopwords, and performs frequency analysis
    to return top N keywords.
    """
    if not text:
        return []
        
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    
    # Filter out stopwords and non-alphabetic tokens
    words = [word for word in tokens if word.isalpha() and word not in stop_words]
    
    fdist = FreqDist(words)
    most_common = fdist.most_common(top_n)
    
    return [word for word, count in most_common]

def generate_tips(keywords):
    """
    Generates study tips dynamically based on extracted keywords.
    """
    tips = []
    if not keywords:
        tips.append("Try breaking your topic down into smaller, manageable chunks.")
        tips.append("Take regular breaks to help retain the information.")
        return tips
        
    tips.append("Make flashcards for these key terms: " + ", ".join(keywords))
    tips.append(f"Create a mind map with '{keywords[0]}' at the center.")
    if len(keywords) > 1:
        tips.append(f"Try to explain how '{keywords[0]}' relates to '{keywords[1]}' to a friend.")
    tips.append("Look for real-world examples and applications for your keywords.")
    tips.append("Test yourself frequently on these topics rather than just re-reading.")
        
    return tips

if __name__ == "__main__":
    sample_topic = "Photosynthesis is a process used by plants to convert light energy into chemical energy."
    kw = extract_keywords(sample_topic)
    print("Extracted Keywords:", kw)
    print("Study Tips:")
    for t in generate_tips(kw):
        print(" -", t)
