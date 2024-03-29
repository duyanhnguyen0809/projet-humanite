import requests
from bs4 import BeautifulSoup
import re
from unidecode import unidecode
from urllib.parse import quote
import json

url = "https://fr.wikipedia.org/wiki/Liste_des_anciennes_communes_des_Alpes-Maritimes"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object from the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the section containing the fusion data
fusion_section = soup.find("span", id="Fusions").find_next("table")

# Extract the data from the table
fusion_data = []
headers = []
for row in fusion_section.find_all("tr"):
    if not headers:
        # Extract the headers from the first row
        headers = [header.text for header in row.find_all("th")]
    else:
        # Extract the data from subsequent rows
        row_data = [data.text for data in row.find_all("td")]
        if row_data:
            row_dict = dict(zip(headers, row_data))
            fusion_data.append(row_dict)
        else:
            # Add the commune name to the previous row's "Communes réunies"
            if fusion_data:
                commune_name = row.find("th").text.strip()
                if fusion_data[-1].get('Communes réunies\n'):
                    fusion_data[-1]['Communes réunies\n'].append(commune_name)
                else:
                    fusion_data[-1]['Communes réunies\n'] = [commune_name]

                # Get the "Date (et nature) de la décision" from the previous row
                prev_row = fusion_data[-1]
                decision = prev_row.get('Date (et nature)\nde la décision\n\n')
                if decision is not None:
                    prev_row['Date (et nature)\nde la décision\n\n'] = decision.strip(
                    )

# Merge the commune names, "Nom de la nouvelle commune", "Communes réunies", and "Date (et nature) de la décision" into a single dictionary
merged_fusion_data = []
for data in fusion_data:
    if 'Nom de la nouvelle\ncommune\n\n' in data:
        merged_dict = {
            'Nom de la nouvelle\ncommune\n\n': data['Nom de la nouvelle\ncommune\n\n'],
            'Communes réunies\n': [data.get('Communes réunies\n')],
            'Date (et nature)\nde la décision\n\n': data.get('Date (et nature)\nde la décision\n\n')
        }
        merged_fusion_data.append(merged_dict)
    else:
        merged_fusion_data[-1]['Communes réunies\n'].append(
            data.get('Communes réunies\n'))

        # Update the "Date (et nature) de la décision" for the previous merged row
        decision = data.get('Date (et nature)\nde la décision\n\n')
        if decision is not None:
            prev_merged_row = merged_fusion_data[-1]
            if 'Date (et nature)\nde la décision\n\n' in prev_merged_row:
                prev_merged_row['Date (et nature)\nde la décision\n\n'] = decision.strip(
                )

final_fusion_data = []
for i in range(len(merged_fusion_data)):
    if merged_fusion_data[i].get('Date (et nature)\nde la décision\n\n') is not None:
        merged_fusion_data[i]['Communes réunies\n'].append(
            merged_fusion_data[i+1].get('Nom de la nouvelle\ncommune\n\n'))
        final_fusion_data.append(merged_fusion_data[i])

for i in range(len(final_fusion_data)):
    final_fusion_data[i] = {k.replace('\n', ' ').rstrip(
    ): v for k, v in final_fusion_data[i].items()}

for i in range(len(final_fusion_data)):
    final_fusion_data[i] = {k: [item.replace('\n', '').rstrip() for item in v] if isinstance(
        v, list) else v.replace('\n', '').rstrip() for k, v in final_fusion_data[i].items()}

for i in range(len(final_fusion_data)):
    final_fusion_data[i] = {k.replace('Date (et nature) de la décision', 'Date'): re.sub(
        r'\[.*?\]', '', v) if k == 'Date (et nature) de la décision' else v for k, v in final_fusion_data[i].items()}

for i in range(len(final_fusion_data)):
    final_fusion_data[i] = {k: re.sub(
        r'(\d{4}).*', r'\1', v) if k == 'Date' else v for k, v in final_fusion_data[i].items()}

for i in range(len(final_fusion_data)):
    final_fusion_data[i] = {
        unidecode(k): v for k, v in final_fusion_data[i].items()}

# for data in final_fusion_data:
#     print(data)
with open('final_fusion_data.json', 'w') as f:
    json.dump(final_fusion_data, f)

# Find the section containing the creation data
creation_section = soup.find("span", id="Créations").find_next("table")


creation_data = []
headers = []
for row in creation_section.find_all("tr"):
    if not headers:
        # Extract the headers from the first row
        headers = [header.text for header in row.find_all("th")]
    else:
        # Extract the data from subsequent rows
        row_data = [data.text for data in row.find_all("td")]
        if row_data:
            row_dict = dict(zip(headers, row_data))
            creation_data.append(row_dict)


for i in range(len(creation_data)):
    creation_data[i] = {k.replace('\n', ' ').rstrip(
    ): v for k, v in creation_data[i].items()}

for i in range(len(creation_data)):
    creation_data[i] = {k: [item.replace('\n', '').rstrip() for item in v] if isinstance(
        v, list) else v.replace('\n', '').rstrip() for k, v in creation_data[i].items()}

for i in range(len(creation_data)):
    creation_data[i] = {k.replace('Date (et nature) de la décision', 'Date'): re.sub(
        r'\[.*?\]', '', v) if k == 'Date (et nature) de la décision' else v for k, v in creation_data[i].items()}

for i in range(len(creation_data)):
    creation_data[i] = {k: re.sub(
        r'(\d{4}).*', r'\1', v) if k == 'Date' else v for k, v in creation_data[i].items()}

for i in range(len(creation_data)):
    creation_data[i] = {unidecode(k): v for k, v in creation_data[i].items()}
grouped_creation_data = {}
for data in creation_data:
    if 'Commune affectee' in data and 'Mode de creation' in data and 'Date' in data:
        key = (data['Commune affectee'],
               data['Mode de creation'], data['Date'])
        if key not in grouped_creation_data:
            # If this key is not already in the grouped_creation_data dictionary, add it with the current data
            grouped_creation_data[key] = data
            # Make sure 'Nom de la commune creee' is a list
            grouped_creation_data[key]['Nom de la commune creee'] = [
                data['Nom de la commune creee']]
        else:
            # If this key is already in the grouped_creation_data dictionary, append the 'Nom de la commune creee' to the existing list
            grouped_creation_data[key]['Nom de la commune creee'].append(
                data['Nom de la commune creee'])
    else:
        # If the current row is missing data, add it to the grouped_creation_data dictionary as is
        grouped_creation_data[data['Nom de la commune creee']] = data

# Replace the original creation_data list with the grouped data
creation_data = list(grouped_creation_data.values())

last_complete_data = None
for i in range(len(creation_data)):
    if 'Commune affectee' in creation_data[i] and 'Mode de creation' in creation_data[i] and 'Date' in creation_data[i]:
        # If the current row has complete data, save it as the last complete data
        last_complete_data = creation_data[i]
        # Make sure 'Nom de la commune creee' is a list
        if not isinstance(last_complete_data['Nom de la commune creee'], list):
            last_complete_data['Nom de la commune creee'] = [
                last_complete_data['Nom de la commune creee']]
    elif last_complete_data is not None:
        # If the current row is missing data and there is a last complete data, append the 'Nom de la commune creee' to the last complete data
        last_complete_data['Nom de la commune creee'].append(
            creation_data[i]['Nom de la commune creee'])
        # Remove the current row from creation_data
        creation_data[i] = None

# Remove None values from creation_data
creation_data = [data for data in creation_data if data is not None]
# for data in creation_data:
#     print(data)
with open('creation_data.json', 'w') as f:
    json.dump(creation_data, f)

# Find the section containing the modification data
modification_section = soup.find(
    "span", id="Modifications_de_nom_officiel").find_next("table")


modification_data = []
headers = []
for row in modification_section.find_all("tr"):
    if not headers:
        # Extract the headers from the first row
        headers = [header.text for header in row.find_all("th")]
    else:
        # Extract the data from subsequent rows
        row_data = [data.text for data in row.find_all("td")]
        if row_data:
            row_dict = dict(zip(headers, row_data))
            modification_data.append(row_dict)


for i in range(len(modification_data)):
    modification_data[i] = {k.replace('\n', ' ').rstrip(
    ): v for k, v in modification_data[i].items()}

for i in range(len(modification_data)):
    modification_data[i] = {k: [item.replace('\n', '').rstrip() for item in v] if isinstance(
        v, list) else v.replace('\n', '').rstrip() for k, v in modification_data[i].items()}

for i in range(len(modification_data)):
    modification_data[i] = {k.replace('Date (et nature) de la décision', 'Date'): re.sub(
        r'\[.*?\]', '', v) if k == 'Date (et nature) de la décision' else v for k, v in modification_data[i].items()}

for i in range(len(modification_data)):
    modification_data[i] = {k: re.sub(
        r'(\d{4}).*', r'\1', v) if k == 'Date' else v for k, v in modification_data[i].items()}

for i in range(len(modification_data)):
    modification_data[i] = {
        unidecode(k): v for k, v in modification_data[i].items()}

last_date = None
for i in range(len(modification_data)):
    if 'Date' in modification_data[i]:
        # If the current row has a date, save it as the last date
        last_date = modification_data[i]['Date']
    elif last_date is not None:
        # If the current row is missing a date and there is a last date, use the last date
        modification_data[i]['Date'] = last_date
    else:
        print(f"Date not found for modification {modification_data[i]}.")
        continue

for data in modification_data:
    print(data)
with open('modification_data.json', 'w') as f:
    json.dump(modification_data, f)

communes = set()

# Extract commune names from the "Modification" table
for data in modification_data:
    communes.add(data['Ancien nom'])
    communes.add(data['Nouveau nom'])

# Extract commune names from the "Creation" table
for data in creation_data:
    if isinstance(data['Nom de la commune creee'], list):
        for commune in data['Nom de la commune creee']:
            communes.add(commune)
    else:
        communes.add(data['Nom de la commune creee'])
    if 'Commune affectee' in data:
        communes.add(data['Commune affectee'])

# Extract commune names from the "Fusion" table
for data in final_fusion_data:
    communes.add(data['Nom de la nouvelle commune'])
    for commune in data['Communes reunies']:
        communes.add(commune)

# Convert the set back to a list of dictionaries

communes = {}

# Extract commune names from the "Modification" table
for data in modification_data:
    ancien_nom = data['Ancien nom']
    nouveau_nom = data['Nouveau nom']
    url = 'https://fr.wikipedia.org/wiki/' + quote(nouveau_nom)
    communes[ancien_nom] = url
    communes[nouveau_nom] = url

# Extract commune names from the "Creation" table
for data in creation_data:
    if isinstance(data['Nom de la commune creee'], list):
        for nom in data['Nom de la commune creee']:
            url = 'https://fr.wikipedia.org/wiki/' + quote(nom)
            communes[nom] = url
    else:
        nom = data['Nom de la commune creee']
        url = 'https://fr.wikipedia.org/wiki/' + quote(nom)
        communes[nom] = url
    if 'Commune affectee' in data:
        nom = data['Commune affectee']
        url = 'https://fr.wikipedia.org/wiki/' + quote(nom)
        communes[nom] = url

# Extract commune names from the "Fusion" table
for data in final_fusion_data:
    nom = data['Nom de la nouvelle commune']
    url = 'https://fr.wikipedia.org/wiki/' + quote(nom)
    communes[nom] = url
    for commune in data['Communes reunies']:
        url = 'https://fr.wikipedia.org/wiki/' + quote(commune)
        communes[commune] = url

# Convert the dictionary back to a list of dictionaries
communes = [{'nom': k, 'url': v} for k, v in communes.items()]

# Print the list of commune names with URLs
# for commune in communes:
#     print(commune)



def dms_to_decimal(dms):
    degrees, minutes, seconds, direction = re.match(
        r"(\d+)°\s(\d+)′\s(\d+)″\s(\w)", dms).groups()
    decimal = round(float(degrees) + float(minutes) /
                    60 + float(seconds)/(60*60), 3)
    if direction in ('S', 'W'):
        decimal *= -1
    return decimal


def get_coordinates(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the coordinates element
    coordinates_element = soup.find("span", id="coordinates")

    # If no coordinates element is found, return None
    if coordinates_element is None:
        return None, None

    # Extract the latitude and longitude values from the coordinates element
    coordinates_text = coordinates_element.find("a").text

    # Parse the latitude and longitude values from the coordinates text
    latitude, longitude = coordinates_text.split(", ")
    latitude = dms_to_decimal(latitude)
    longitude = dms_to_decimal(longitude)

    return latitude, longitude

for i in range(len(communes)):
    url = communes[i]['url']
    lat, lon = get_coordinates(url)
    communes[i]['lat'] = lat
    communes[i]['lon'] = lon

# Save the list of commune names with URLs and coordinates to a JSON file
with open('communes.json', 'w') as f:
    json.dump(communes, f)

# # Print the list of commune names with URLs and coordinates
# for commune in communes:
#     print(commune)

# Load the JSON file
with open('communes.json', 'r') as file:
    data = json.load(file)

