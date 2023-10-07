import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import string
import gensim
import nltk
import plotly.graph_objs as go
from gensim import corpora
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import csv
import plotly
import plotly.io as pio
import plotly.offline as pyo
from nltk.corpus import wordnet as wn
from flask import session

# Function to create a CSV file for selected country
def create_csv_for_selected_country(country_code, folder_path, csv_filename):
    csv_file = open(csv_filename, 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Country Code', 'Year', 'Text'])

    for filename in os.listdir(folder_path):
        if filename.startswith(country_code) and filename.endswith('.txt'):
            # Extract year from the filename
            year = filename.split('_')[-1].split('.')[0]

            # Read the content of the file
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                text = file.read()

            # Write the data to the CSV file
            csv_writer.writerow([country_code, year, text])

    # Close the CSV file
    csv_file.close()


# Function to preprocess text data
def preprocess_text(text):
    # Convert text to lowercase and replace non-alphanumeric characters with spaces
    text = text.lower()
    text = re.sub('\W+', ' ', text)
    
    # Replace "united nations" with "united_nations"
    text = re.sub('united nations', 'united_nations', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Define a set of stopwords to remove
    stop_words = set(stopwords.words('english'))
    stop_words.add("'s")
    stop_words.add("'")
    stop_words.add("-")
    
    # Remove stopwords and punctuation
    clean_tokens = [w for w in tokens if not w in stop_words and not w in string.punctuation]
    
    # Lemmatize the tokens
    def get_lemma(word):
        lemma = wn.morphy(word)
        if lemma is None:
            return word
        else:
            return lemma

    lemmatized_tokens = [get_lemma(token) for token in clean_tokens]
    
    return lemmatized_tokens

# Function to calculate word frequencies
def calculate_word_frequencies(debates):
    freqs = {}
    for i, speech in debates.iterrows():
        year = speech['Year']
        for token in speech['stems']:
            if token not in freqs:
                freqs[token] = {"total_freq": 1, year: 1}
            else:
                freqs[token]["total_freq"] += 1
                if not freqs[token].get(year):
                    freqs[token][year] = 1
                else:
                    freqs[token][year] += 1
    freqs_df = pd.DataFrame.from_dict(freqs, orient='index')
    freqs_df['word'] = freqs_df.index
    new_cols = ["total_freq", "word"] + sorted(freqs_df.columns.tolist()[1:-1])
    freqs_df = freqs_df[new_cols]
    freqs_df = freqs_df.sort_values('total_freq', ascending=False)
    freqs_df = freqs_df.fillna(0)
    return freqs_df

# Function to process and visualize text data
def process_and_visualize_text(data_frame, top_n=100):
    # Calculate additional text metrics
    data_frame['char_count'] = data_frame['Text'].str.len()
    data_frame['words'] = data_frame['Text'].str.split(' ')
    data_frame['sentences'] = data_frame['Text'].str.split('.')
    data_frame['word_count'] = data_frame['words'].str.len()
    data_frame['sentence_count'] = data_frame['sentences'].str.len()
    data_frame['word_length'] = data_frame['char_count'] / data_frame['word_count']
    data_frame['sentence_length'] = data_frame['word_count'] / data_frame['sentence_count']

    # Preprocess the text data
    data_frame['Text'] = data_frame['Text'].str.lower().map(lambda x: re.sub('\W+', ' ', x))
    data_frame['Text'] = data_frame['Text'].str.lower().map(lambda x: re.sub('united nations', 'united_nations', x))
    data_frame['token'] = data_frame['Text'].apply(word_tokenize)
    stop_words = set(stopwords.words('english'))
    stop_words.add("'s")
    stop_words.add("'")
    stop_words.add("-")
    data_frame['clean'] = data_frame['token'].apply(lambda x: [w for w in x if not w in stop_words and not w in string.punctuation])

    # Lemmatization
    def get_lemma(word):
        lemma = wn.morphy(word)
        if lemma is None:
            return word
        else:
            return lemma

    data_frame['stems'] = [[format(get_lemma(token)) for token in speech] for speech in data_frame['clean']]
    data_frame = data_frame.sort_values('Year')

    # Create a dictionary to store word frequencies
    freqs = {}

    # Iterate through the speeches in the DataFrame
    for i, speech in data_frame.iterrows():
        year = speech['Year']
        for token in speech['stems']:
            if token not in freqs:
                freqs[token] = {"total_freq": 1, year: 1}
            else:
                freqs[token]["total_freq"] += 1
                if not freqs[token].get(year):
                    freqs[token][year] = 1
                else:
                    freqs[token][year] += 1

    # Convert the frequency data to a DataFrame
    freqs_df = pd.DataFrame.from_dict(freqs, orient='index')
    freqs_df['word'] = freqs_df.index
    new_cols = ["total_freq", "word"] + sorted(freqs_df.columns.tolist()[1:-1])
    freqs_df = freqs_df[new_cols]
    freqs_df = freqs_df.sort_values('total_freq', ascending=False)
    freqs_df = freqs_df.fillna(0)

    # Return the processed data
    return freqs_df


# Function to train an LDA model
def train_lda_model(text_data, num_topics=10, passes=15):
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
    ldamodel.save('model10.gensim')
    return ldamodel
create_csv_for_selected_country('IND', 'Capstone_UN_dataset/dataverse_files/Final', 'output.csv')
# Load the CSV file created in the previous step
data = pd.read_csv('output.csv')

# Preprocess the text data and store the results in 'stems' column
data['stems'] = data['Text'].apply(preprocess_text)

# Process and visualize text data
process_and_visualize_text(data)

# Train an LDA model
lda_model = train_lda_model(data['stems'], num_topics=10, passes=15)


# Calculate word frequencies
word_frequencies = calculate_word_frequencies(data)

# Print the top word frequencies
print(word_frequencies.head())

common_words = word_frequencies.iloc[0:5, 1:47].transpose().iloc[1:]
common_words.plot(kind='line', title="Most Common Words", figsize=(16, 8))
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.show()

