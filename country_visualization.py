import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator
import topic_modeling

def analyze_and_plot_data(data, topic_list, country_list, colors):
    # Calculate the number of speeches per country
    countries = data['year'].groupby(data['countrycode']).count()
    countries = pd.DataFrame(countries.reset_index(drop=False))
    countries.columns = ['countrycode', 'num speeches']

    # Find the most vocal member nations
    max_num_speeches = countries['num speeches'].max()
    most_vocal_countries = countries[countries['num speeches'] == max_num_speeches].countrycode.unique()

    # Find the least vocal member nations
    min_num_speeches = countries['num speeches'].min()
    least_vocal_countries = countries.countrycode[:10].unique().tolist()

    print('Most Vocal Member Nations')
    print('max number of speeches given:', max_num_speeches)
    print(most_vocal_countries)
    print()

    print('Least Vocal Member Nations')
    print('min number of speeches given:', min_num_speeches)
    print(least_vocal_countries)

    # Function to calculate and plot frequency of topic mentions
    def freq_mentioned(df, country_list, topic_list, colors):
        data = df.loc[df['countrycode'].isin(country_list)].copy()

        for i in topic_list:
            data[i] = data['text'].str.contains(i)
            data.loc[data[i] == False, i] = np.nan

        country = country_list[0]
        data_out = pd.DataFrame(data.loc[data['countrycode'] == country].count())
        data_out = (data_out.T)[topic_list]

        countries = country_list.copy()
        countries.remove(country)

        for i in countries:
            a = pd.DataFrame(data.loc[data['countrycode'] == i].count())
            a = (a.T)[topic_list].copy()
            data_out = pd.concat([data_out, a], axis=0)

        dictionary = {}

        for i in topic_list:
            dictionary[i] = data_out[i].sum()

        sorted_dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
        data_out = data_out[[i[0] for i in sorted_dictionary]]
        data_out.index = country_list
        data_out.T.plot(kind="barh", width=.6, stacked=True, figsize=(10, len(topic_list) / 3), color=colors).legend(
            bbox_to_anchor=(1, 1))

        plt.show()  # Display the plot

        return data_out

    # Perform the analysis and plotting
    freq_mentioned(data, country_list, topic_list, colors)

if __name__ == "__main__":
    # Define your parameters
    folder_path = '/Users/asmitashelke/Desktop/Project/Capstone_UN_dataset/dataverse_files/Final'
    csv_filename = 'output.csv'

    # Extract data to CSV and analyze data
    topic_modeling.extract_data_to_csv(folder_path, csv_filename)
    data = pd.read_csv(csv_filename)

    # Define topics, countries, and colors
    topics = ['amnesty', 'universal jurisdiction', 'transitional justice', 'civil war', 'truth commission', 'intervention', 'communism', 'communist', 'evil', 'unjust',
              'peacekeeping', 'trial', 'justice cascade', 'truth seeking', 'invasion', 'reparations', 'extradition', 'memorial', 'dictatorship', 'fascist', 'fascism', 'injustice',
              'prosecution', 'rule of law', 'vetting', 'lustration', 'disarmament', 'demobilization', 'reintegration', 'strength', 'weakness', 'strongman', 'dictator',
              'forgiveness', 'institutional reform', 'reconciliation', 'genocide', 'hague', 'war crime', 'war crimes', 'human rights', 'TRC', 'amnesties', 'democracy', 'democratic',
              'crime against humanity', 'immunity', 'sovereign immunity', 'sovereign', 'exile', 'restorative', 'tribunal', 'Rome Statute', 'illegal', 'international law',
              'justice', 'victims', 'perpetrators', 'resistance', 'military intervention', 'non-intervention', 'isolationist', 'due process', 'sovereignty', 'democratization',
              'isolationism', 'internationalist', 'tolerance', 'nuremburg', 'sanctions', 'crimes against humanity', 'sanction', 'backslide', 'backsliding']

    countries = ['AUS', 'NZL', 'CHN', 'JPN', 'VNM', 'KOR', 'PRK', 'IDN', 'SGP', 'MAL', 'TMP', 'THA']

    colors = ['dodgerblue', 'orange', 'navy', 'lightseagreen', 'yellow', 'green', 'blue', 'maroon', 'purple', 'peru',
              'violet', 'tomato', 'skyblue']

    # Call the function to perform the analysis and plotting
    analyze_and_plot_data(data, topics, countries, colors)
