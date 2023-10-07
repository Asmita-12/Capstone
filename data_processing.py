import os
import string
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.corpus import stopwords
import pandas as pd

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Additional words to remove
additional_stop_words = set(['would', 'organization', 'assembly', 'human', 'global', 'united', 'countries', 'nations', 'international', 'world', 'development', 'peace', 'states', 'people', 'security', 'economic', 'peoples', 'also', 'new', 'must', 'government'])
stop_words = set(stopwords.words('english'))
stop_words.update(additional_stop_words)
# Define the function to preprocess the text
def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ''.join(c for c in text if not c.isdigit())
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in stop_words and token not in additional_stop_words]
    tokens = [token for token in tokens if token.isalpha()]
    return tokens

def process_directory(dir_path):
    year_word_counts = {}
    
    for folder in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, folder)):
            year = folder.split(' ')[-1]
            word_counts = Counter()
            for file_name in os.listdir(os.path.join(dir_path, folder)):
                with open(os.path.join(dir_path, folder, file_name), 'r', encoding='latin1') as file:
                    text = file.read()
                    tokens = preprocess_text(text)
                    word_counts.update(tokens)
            year_word_counts[year] = word_counts
    
    return year_word_counts

def visualize_temporal_ranking_funnel(year_word_counts, year, n=10):
    word_counts = year_word_counts[year]
    top_words = dict(word_counts.most_common(n))

    word_freqs = list(top_words.values())
    max_freq = max(word_freqs)
    bar_lengths = [int((freq / max_freq) * 20) for freq in word_freqs]

    plt.figure(figsize=(10, 6))
    sns.barplot(x=bar_lengths, y=list(top_words.keys()), palette='viridis')
    plt.title(f'Funnel-Shaped Temporal Ranking of Top {n} Words - Year {year}')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.show()

def word_evolution_over_years(year_word_counts, word):
    evolution = {}
    
    for year, word_counts in year_word_counts.items():
        if word in word_counts:
            evolution[year] = word_counts[word]
        else:
            evolution[year] = 0
    
    return evolution

def visualize_word_evolution(word_evolution, word):
    years = sorted(list(word_evolution.keys()))
    word_freqs = list(word_evolution.values())

    plt.figure(figsize=(12, 6))
    plt.plot(years, word_freqs, marker='o', linestyle='-')
    plt.title(f'Evolution of the Word Frequency: "{word}" Over the Years')
    plt.xlabel('Year')
    plt.ylabel('Word Frequency')
    plt.xticks(rotation=45)  # Rotate x-axis labels by 45 degrees
    plt.tight_layout()  # Adjust layout to prevent label overlap
    plt.grid(True)
    plt.show()

# Example usage for generating the funnel-shaped visualization and word evolution
if __name__ == "__main__":
    folder_path = '/Users/asmitashelke/Desktop/Project/Capstone_UN_dataset/dataverse_files/TXT'
    year_word_counts = process_directory(folder_path)
    visualize_temporal_ranking_funnel(year_word_counts, '2000', n=10)
    word_evolution = word_evolution_over_years(year_word_counts, 'climate')
    visualize_word_evolution(word_evolution, 'climate')
