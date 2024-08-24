import requests
from bs4 import BeautifulSoup
import csv

def scrape_warframe_wiki(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Initialize an empty dictionary to store the relevant sections
    data = {'title': '', 'acquisition': '', 'crafting': '', 'vaulting': '', 'abilities': ''}

    # Extract the title
    title = soup.find('h1', class_='page-header__title').text.strip()
    data['title'] = title

    # Scrape the Main section - Acquisition and Crafting
    main_section = soup.find(id='Main')
    if main_section:
        acquisition = main_section.find('span', id='Acquisition').find_next('p').text.strip()
        crafting = main_section.find('span', id='Crafting').find_next('p').text.strip()
        data['acquisition'] = acquisition
        data['crafting'] = crafting

    # Scrape the Prime section - Acquisition, Vaultings, Crafting
    prime_section = soup.find(id='Prime')
    if prime_section:
        acquisition_prime = prime_section.find('span', id='Acquisition').find_next('p').text.strip()
        vaultings_prime = prime_section.find('span', id='Vaultings').find_next('p').text.strip()
        crafting_prime = prime_section.find('span', id='Crafting').find_next('p').text.strip()
        data['acquisition'] += '\n' + acquisition_prime
        data['vaulting'] = vaultings_prime
        data['crafting'] += '\n' + crafting_prime

    # Scrape the Abilities section - Scrape the whole page other than comments
    abilities_section = soup.find(id='Abilities')
    if abilities_section:
        abilities = []
        for element in abilities_section.find_all(['p', 'h2', 'h3', 'h4', 'ul', 'ol', 'table']):
            # Skip comments if they exist
            if not element.find(class_='comment'):
                abilities.append(element.text.strip())
        data['abilities'] = '\n'.join(abilities)

    return data

# List of URLs to scrape
urls = [
    'https://warframe.fandom.com/wiki/Ash',
    'https://warframe.fandom.com/wiki/Octavia',
    # Add more URLs as needed
]

# Scrape data and save to CSV
with open('warframe_data_filtered.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['title', 'acquisition', 'crafting', 'vaulting', 'abilities'])
    writer.writeheader()
    for url in urls:
        data = scrape_warframe_wiki(url)
        writer.writerow(data)