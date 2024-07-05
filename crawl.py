import os
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import pandas as pd

def parse_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        # Extract data from the HTML file, customize this as per your needs
        title = soup.title.string if soup.title else ''
        meta_desc = soup.find("meta", attrs={
            "name":"description"
        })["content"]
        
        # remove next pages
        content = soup.find("div", attrs={
            "id":"city"
        })
        
        next_top = content.find("div", attrs={
            "id":'bottomnextup',
        })
        next_bottom = content.find("div", attrs={
            "id":'bottomnext',
        })
        next_topic_div = content.find("div", attrs={
            "class":'nexttopicdiv',
        })
        next_top.extract()
        next_bottom.extract()
        next_topic_div.extract()
        # Add more fields as required
        return {
            'title': title,
            "meta_desc": meta_desc,
            "body": content
        }

def main(folder_path, output_csv):
    html_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.html')]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(parse_html, html_files))

    # Convert results to a DataFrame and save to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)

if __name__ == '__main__':
    folder_path = './blog'  # Specify the folder containing HTML files
    output_csv = 'result/output.csv'  # Specify the output CSV file name
    main(folder_path, output_csv)
