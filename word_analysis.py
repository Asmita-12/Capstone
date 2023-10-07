import os
import string
from collections import Counter
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

additional_stop_words = set(['organization', 'assembly', 'human', 'global', 'united', 'countries', 'nations',
                             'international', 'world', 'peace', 'states', 'people', 'peoples', 'also', 'new', 'must',
                             'government'])

topics = ['amnesty', 'universal jurisdiction', 'transitional justice', 'civil war', 'truth commission', 'intervention', 'communism', 'communist', 'evil', 'unjust',
              'peacekeeping', 'trial', 'justice cascade', 'truth seeking', 'invasion', 'reparations', 'extradition', 'memorial', 'dictatorship', 'fascist', 'fascism', 'injustice',
              'prosecution', 'rule of law', 'vetting', 'lustration', 'disarmament', 'demobilization', 'reintegration', 'strength', 'weakness', 'strongman', 'dictator',
              'forgiveness', 'institutional reform', 'reconciliation', 'genocide', 'hague', 'war crime', 'war crimes', 'human rights', 'TRC', 'amnesties', 'democracy', 'democratic',
              'crime against humanity', 'immunity', 'sovereign immunity', 'sovereign', 'exile', 'restorative', 'tribunal', 'Rome Statute', 'illegal', 'international law',
              'justice', 'victims', 'perpetrators', 'resistance', 'military intervention', 'non-intervention', 'isolationist', 'due process', 'sovereignty', 'democratization',
              'isolationism', 'internationalist', 'tolerance', 'nuremburg', 'sanctions', 'crimes against humanity', 'sanction', 'backslide', 'backsliding']

def preprocess_text(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ''.join(c for c in text if not c.isdigit())
    tokens = nltk.word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in stop_words and token not in additional_stop_words]
    tokens = [token for token in tokens if token.isalpha()]
    return tokens

def load_word_frequencies(dir_path):
    word_frequencies = {}

    for folder in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, folder)):
            year = folder.split(' ')[-1]
            word_counts = Counter()
            for file_name in os.listdir(os.path.join(dir_path, folder)):
                with open(os.path.join(dir_path, folder, file_name), 'r', encoding='latin1') as file:
                    text = file.read()

                tokens = preprocess_text(text)
                word_counts.update(tokens)
                word_frequencies[year] = word_counts

    return word_frequencies

def plot_word_frequency(word_frequencies, target_word):
    frequencies = []

    for year in range(1970, 2023):
        year_str = str(year)
        if year_str in word_frequencies and target_word in word_frequencies[year_str]:
            frequencies.append(word_frequencies[year_str][target_word])
        else:
            frequencies.append(0)
    print(f"Frequencies for '{target_word}': {frequencies}")
    # Return the frequencies data
    return frequencies

def get_topic_list():
    return topics

if __name__ == "__main__":
    dir_path = "Capstone_UN_dataset/dataverse_files/TXT"
    word_frequencies = load_word_frequencies(dir_path)
    target_word = "pandemic"
    plot_word_frequency(word_frequencies, target_word)
