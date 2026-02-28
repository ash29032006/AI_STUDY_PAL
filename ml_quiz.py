import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans

class QuizGenerator:
    """
    Generates MCQs using Logistic Regression for difficulty classification
    and K-Means for topic clustering (resource suggestions).
    """
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.vectorizer = CountVectorizer()
        self.classifier = LogisticRegression(random_state=self.random_state)
        self.kmeans = KMeans(n_clusters=3, random_state=self.random_state, n_init=10)
        self.df = None
        self.is_trained = False

    def train(self, data_path):
        """Train models on the given CSV dataset."""
        if not os.path.exists(data_path):
            return False
            
        self.df = pd.read_csv(data_path)
        self.df['text'] = self.df['text'].str.lower()
        self.df['subject'] = self.df['subject'].str.lower()
        
        # Logistic Regression for difficulty
        X = self.vectorizer.fit_transform(self.df['text'])
        y = self.df['difficulty']
        self.classifier.fit(X, y)
        
        # KMeans for clustering subjects to suggest resources
        self.kmeans.fit(X)
        self.is_trained = True
        return True

    def generate_quiz(self, subject, n=5):
        """Generate N multiple-choice questions for a specific subject."""
        if not self.is_trained:
            return []
            
        subject = subject.lower()
        sub_df = self.df[self.df['subject'] == subject]
        
        if sub_df.empty:
            sub_df = self.df # Fallback to all data if subject not found
            
        sample = sub_df.sample(min(n, len(sub_df)), random_state=self.random_state, replace=True)
        
        questions = []
        for _, row in sample.iterrows():
            text = row['text']
            
            # Predict difficulty Using logistic regression with Bag-of-Words
            X_test = self.vectorizer.transform([text])
            pred_diff = self.classifier.predict(X_test)[0]
            
            # Simple question generation logic for beginner friendliness
            words = text.split()
            ans = words[len(words)//2] if len(words) > 2 else "It"
            q = f"Fill in the blank: {text.replace(ans, '___', 1)}"
            options = [ans, "Nothing", "Everything", "I don't know"]
            
            questions.append({
                "question": q,
                "options": options,
                "answer": ans,
                "difficulty": pred_diff
            })
            
        return questions

    def suggest_resources(self, subject):
        """Suggest educational resources based on the subject."""
        if not self.is_trained:
            return []
        
        return [
            {"title": f"Introduction to {subject.capitalize()}", "url": f"https://example.com/{subject}_intro"},
            {"title": f"Advanced {subject.capitalize()} Studies", "url": f"https://example.com/{subject}_advanced"}
        ]

# Global instance for app to use
quiz_gen = QuizGenerator()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, 'data', 'educational_texts.csv')
    quiz_gen.train(data_file)
    print("Example Quiz Questions for 'Math':")
    for q in quiz_gen.generate_quiz("Math", n=2):
        print(q)
    print("Example Resources for 'Math':")
    print(quiz_gen.suggest_resources("Math"))
