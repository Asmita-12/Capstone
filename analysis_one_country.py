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
from nltk.corpus import wordnet as wn
import analysis_one_category

def plot_category(category, freqs_df):
    categories = {
        'war_and_peace': ['peace', 'war', 'security', 'cold', 'conflict', 'aggression'],
        'economy': ['economy', 'wealth', 'crisis', 'growth', 'inflation', 'trade', 'poverty', 'rich', 'income'],
        'people': ['people', 'refugee', 'humanitarian', 'freedom', 'right'],
        'politics': ['democracy', 'republic', 'dictator', 'sovereign', 'politics'],
        'environment': ['environment', 'sustain', 'green', 'energy', 'ecology', 'warm', 'temperature', 'pollution', 'planet'],
        'terrorism': ['terror', 'terrorism', 'terrorist']
    }

    if category not in categories:
        print("Invalid category")
        return

    words = categories[category]
    title = category.capitalize()

    # Filter the data for the selected words
    filtered_data = freqs_df[freqs_df['word'].isin(words)].iloc[:, 1:47].transpose().iloc[1:]

    # Plot the data
    return filtered_data

# Call the function with the desired category (e.g., 'terrorism')
plot_category('terrorism', analysis_one_category.word_frequencies)
