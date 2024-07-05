import os
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import pandas as pd

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        # Extract data from the HTML file, customize this as per your needs
        title = soup.title.string if soup.title else 'No Title'
        # Add more fields as required
        return {'file': file_path, 'title': title}

def main(folder_path, output_csv):
    html_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.html')]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(parse_html, html_files))

    # Convert results to a DataFrame and save to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

if __name__ == '__main__':
    folder_path = 'path/to/your/html/folder'  # Specify the folder containing HTML files
    output_csv = 'output.csv'  # Specify the output CSV file name
    main(folder_path, output_csv)
