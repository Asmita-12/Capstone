import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator

def clean_text(text):
    if text is not None:
        # Add your text cleaning logic here
        # For example, remove special characters, stopwords, etc.
        # Return the cleaned text
        return text
    else:
        return ''  # Replace null values with an empty string

def extract_data_to_csv(folder_path, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL, escapechar='\\')
        csv_writer.writerow(['countrycode', 'session', 'year', 'text'])

        for filename in os.listdir(folder_path):
            if filename.endswith('.txt'):
                parts = filename.split('_')
                if len(parts) == 3:
                    country_code, session, year = parts
                    year = year.split('.')[0]
                    with open(os.path.join(folder_path, filename), 'r', encoding='utf-8', errors='replace') as file:
                        text = file.read()
                        text = clean_text(text)
                    csv_writer.writerow([country_code, session, year, text])

    print(f'Conversion completed. The CSV file "{csv_filename}" has been created.')

def analyze_data(csv_filename):
    data = pd.read_csv(csv_filename)
    data['text'] = data['text'].str.lower()

    # Drop rows with NaN values in the 'year' column
    data.dropna(subset=['year'], inplace=True)

    # Convert 'year' column to numeric, setting errors='coerce' to handle non-numeric values
    data['year'] = pd.to_numeric(data['year'], errors='coerce')

    # Filter the data for valid years greater than 1970
    data = data[data['year'] > 1970]

    data['char_count'] = data['text'].str.len()
    data['words'] = data['text'].str.split(' ')
    data['sentences'] = data['text'].str.split('.')
    data['word_count'] = data['words'].str.len()
    data['sentence_count'] = data['sentences'].str.len()
    data['word_length'] = data['char_count'] / data['word_count']
    data['sentence_length'] = data['word_count'] / data['sentence_count']

    topics = ['amnesty', 'universal jurisdiction', 'transitional justice', 'civil war', 'truth commission', 'intervention', 'communism', 'communist', 'evil', 'unjust',
              'peacekeeping', 'trial', 'justice cascade', 'truth seeking', 'invasion', 'reparations', 'extradition', 'memorial', 'dictatorship', 'fascist', 'fascism', 'injustice',
              'prosecution', 'rule of law', 'vetting', 'lustration', 'disarmament', 'demobilization', 'reintegration', 'strength', 'weakness', 'strongman', 'dictator',
              'forgiveness', 'institutional reform', 'reconciliation', 'genocide', 'hague', 'war crime', 'war crimes', 'human rights', 'TRC', 'amnesties', 'democracy', 'democratic',
              'crime against humanity', 'immunity', 'sovereign immunity', 'sovereign', 'exile', 'restorative', 'tribunal', 'Rome Statute', 'illegal', 'international law',
              'justice', 'victims', 'perpetrators', 'resistance', 'military intervention', 'non-intervention', 'isolationist', 'due process', 'sovereignty', 'democratization',
              'isolationism', 'internationalist', 'tolerance', 'nuremburg', 'sanctions', 'crimes against humanity', 'sanction', 'backslide', 'backsliding']

    dictionary = {}

    for i in topics:
        # Ensure that 'year' is not NaN before using boolean indexing
        dictionary[i] = data['year'][data['year'].notna() & data['text'].str.contains(i)].count() / len(data) * 100

    sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)

    labels = [i[0] for i in sorted_dictionary]
    values = [i[1] for i in sorted_dictionary]
    xs = np.arange(len(labels))

    width = 0.85
    plt.figure(figsize=(18, 9))
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.tick_params(axis='both', which='minor', labelsize=12)
    plt.xticks(rotation=80)
    plt.xlabel('Topics')
    plt.ylabel('% of Debates Mentioned')
    plt.title('Bar Plot of Topics Mentioned')

    plt.bar(xs, values, width, align='center')
    plt.xticks(xs, labels)
    plt.show()

if __name__ == "__main__":
    folder_path = '/Users/asmitashelke/Desktop/Project/Capstone_UN_dataset/dataverse_files/Final'
    csv_filename = 'output.csv'

    extract_data_to_csv(folder_path, csv_filename)
    analyze_data(csv_filename)

