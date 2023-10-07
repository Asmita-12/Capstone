from flask import Flask, render_template, request, redirect, url_for, session, Response
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend which doesn't require a GUI
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from word_analysis import get_topic_list, plot_word_frequency, load_word_frequencies

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Import necessary functions from analysis_one_category.py
from hello import get_unique_countries_with_iso_codes
from analysis_one_category import create_csv_for_selected_country, process_and_visualize_text

# Replace the file path with your Excel file
file_path = "Capstone_UN_dataset/dataverse_files/Speakers_by_session.xlsx"

# Function to get unique countries with ISO Codes
def get_unique_countries_with_iso():
    unique_countries_with_iso = get_unique_countries_with_iso_codes(file_path)
    return unique_countries_with_iso

@app.route('/')
def front_page():
    return render_template('front_page.html')

@app.route('/word_analysis_topic_list', methods=['GET', 'POST'])
def word_analysis_topic_list():
    if request.method == 'POST':
        selected_topic = request.form.get('selected_topic')
        return redirect(url_for('word_analysis_visual', selected_topic=selected_topic))
    return render_template('word_analysis_topic_list.html', topics=get_topic_list())

@app.route('/word_analysis_visual/<selected_topic>')
def word_analysis_visual(selected_topic):
    # Process and visualize text
    dir_path = "Capstone_UN_dataset/dataverse_files/TXT"
    word_frequencies = load_word_frequencies(dir_path)

    # Call the plot_word_frequency function and capture the plot data
    frequencies = plot_word_frequency(word_frequencies, selected_topic)

    # Customize the plot (optional)

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.figure(figsize=(10, 6))
    plt.plot(range(1970, 2023), frequencies, marker='o')
    plt.title(f"Frequency of '{selected_topic}' in UN Speeches (1970-2022)")
    plt.xlabel("Year")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.xticks(range(1970, 2023), rotation=45)
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the Matplotlib plot image data as base64
    image_data = base64.b64encode(buffer.read()).decode('utf-8')

    # Pass the selected topic, Matplotlib plot image, and processed data to the template
    return render_template('word_analysis_visual.html', selected_topic=selected_topic, image=image_data, frequencies=frequencies)


@app.route('/country_analysis')
def country_analysis():
    # Add your country analysis code here
    countries_with_iso = get_unique_countries_with_iso()
    return render_template('index.html', countries_with_iso=countries_with_iso)

@app.route('/store_iso', methods=['POST'])
def store_iso():
    selected_iso = request.form.get('iso')
    session['selected_iso_code'] = selected_iso

    # Pass the selected ISO code as a query parameter
    return redirect(url_for('visualize', iso_code=selected_iso))

@app.route('/visualize')
def visualize():
    # Retrieve the selected ISO Code from the session
    selected_iso_code = session.get('selected_iso_code')

    # Pass the selected ISO code to the create_csv_for_selected_country function
    create_csv_for_selected_country(selected_iso_code, 'Capstone_UN_dataset/dataverse_files/Final', 'output.csv')

    # Process and visualize text
    data = pd.read_csv('output.csv')  # Load your data into a DataFrame
    freqs_df = process_and_visualize_text(data, top_n=100)  # Get the processed data

    # Plot the graph using the processed data
    plt.figure()
    plt.plot(freqs_df.iloc[0:10]['word'], freqs_df['total_freq'][0:10])
    plt.title('Word Frequency Plot')

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Encode the Matplotlib plot image data as base64
    image_data = base64.b64encode(buffer.read()).decode('utf-8')

    # Pass the selected ISO code, Matplotlib plot image, and processed data to the template
    return render_template('next_page.html', selected_iso=selected_iso_code, image=image_data, freqs_data=freqs_df.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
