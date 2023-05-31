import json
from bs4 import BeautifulSoup
import os

def html_to_json(html_file, output_file):
    # Read the HTML file
    with open(html_file, 'r') as file:
        html_data = file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_data, 'html.parser')

    # Extract the desired data from the HTML
    # Modify this part according to your specific requirements

    # Get the title if it exists, otherwise set it to None
    title = soup.title.string if soup.title else None

    # Get the body text if it exists, otherwise set it to None
    body = soup.body.get_text() if soup.body else None

    # Create a list to store the extracted links
    links = []
    for link in soup.find_all('a'):
        if 'href' in link.attrs:
            links.append(link['href'])

    # Create a dictionary to store the extracted data
    data = {
        'title': title,
        'body': body,
        'links': links
    }

    # Convert the data to JSON format
    json_data = json.dumps(data, indent=4)

    # Write the JSON data to the output file
    with open(output_file, 'w') as file:
        file.write(json_data)

# Folder path containing HTML files
folder_path = 'crawled_pages'

# Output folder for JSON files
output_folder = 'jsons'

count = 0
# Iterate over HTML files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        # Create input and output file paths
        html_file = os.path.join(folder_path, filename)
        json_name = "page" + str(count) + ".json"
        json_file = os.path.join(output_folder, json_name)
        count += 1

        # Convert HTML to JSON
        html_to_json(html_file, json_file)
