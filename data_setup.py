import pandas as pd
import matplotlib.pyplot as plt
import os

def clean_data(file_path):
    """
    Load, clean (lowercase, remove duplicates), and return the DataFrame.
    """
    df = pd.read_csv(file_path)
    df.drop_duplicates(inplace=True)
    df['text'] = df['text'].str.lower()
    df['subject'] = df['subject'].str.lower()
    return df

def plot_distribution(df, output_path):
    """
    Plot the subject distribution pie chart and save as PNG.
    """
    counts = df['subject'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Educational Texts by Subject')
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, 'data', 'educational_texts.csv')
    output_png = os.path.join(current_dir, 'subject_distribution.png')
    
    if os.path.exists(data_file):
        df_cleaned = clean_data(data_file)
        plot_distribution(df_cleaned, output_png)
        print(f"Data cleaned. Shape: {df_cleaned.shape}")
        print(f"Distribution plot saved to {output_png}")
    else:
        print(f"Data file not found: {data_file}")
