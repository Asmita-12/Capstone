import os
import shutil
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet as wn
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import string
from collections import Counter
import seaborn as sns
import csv
import re
import plotly.graph_objs as go
import plotly.offline
from plotly.offline import iplot
from gensim import corpora, models
import gensim


#%matplotlib inline

# Define the folder path on your local machine
folder_path = 'Capstone_UN_dataset/dataverse_files/Final'

# Get a list of files in the folder
files = os.listdir(folder_path)

# Print the list of files
#print(files)

posts = pd.read_excel("Capstone_UN_dataset/dataverse_files/Speakers_by_session.xlsx")

# Create a frequency table of the "Post" column
table = pd.value_counts(posts['Post'])

# Print the frequency table
#print(table)

## ************************************************Find most frequent words using frequency**************************************************** 

# Download the stopwords corpus
nltk.download('stopwords', quiet=True, raise_on_error=False)
stop_words = set(stopwords.words('english'))

# Additional words to remove
additional_stop_words = set(['would','organization', 'assembly', 'human', 'global', 'united', 'country','community','countries', 'one','us','efforts','general', 'nations', 'international', 'world', 'development', 'peace', 'states', 'people', 'security', 'economic', 'peoples', 'also', 'new', 'must', 'government'])

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
    
    sorted_years = sorted(year_word_counts.keys())
    
    results = {}
    for year in sorted_years:
        word_counts = year_word_counts[year]
        most_common_word = word_counts.most_common(1)[0][0]
        results[year] = most_common_word
    
    return results

# Example usage: (use when front end is ready)
#result_words = process_directory("Capstone_UN_dataset/dataverse_files/TXT")
#print(result_words)
 ##*****************************************Find Unique Countries****************************************************


import pandas as pd

def get_unique_countries_with_iso_codes(file_path):
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)

        # Extract unique country names and ISO Codes
        unique_countries_with_iso = df[['Country', 'ISO Code']].drop_duplicates()

        return unique_countries_with_iso.values.tolist()
    except Exception as e:
        return str(e)

# Example usage:
if __name__ == "__main__":
    file_path = "Capstone_UN_dataset/dataverse_files/Speakers_by_session.xlsx"  # Replace with the path to your Excel file
    unique_countries_with_iso = get_unique_countries_with_iso_codes(file_path)
    print(unique_countries_with_iso)


##***********************************Visualization to find 10 most frequent used words every year************************************* 

nltk.download('punkt')
nltk.download('stopwords')

additional_stop_words = set(['would', 'organization', 'assembly', 'human', 'global', 'united', 'countries', 'nations', 'international', 'world', 'development', 'peace', 'states', 'people', 'security', 'economic', 'peoples', 'also', 'new', 'must', 'government'])

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

def visualize_word_evolution(word_evolution,word):
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
year_word_counts = process_directory("/Users/asmitashelke/Desktop/Project/Capstone_UN_dataset/dataverse_files/TXT")
visualize_temporal_ranking_funnel(year_word_counts, '2000', n=10)
word_evolution = word_evolution_over_years(year_word_counts, 'climate')
visualize_word_evolution(word_evolution,'climate')


## **********************************************Analysis of one particular country ****************************************************

