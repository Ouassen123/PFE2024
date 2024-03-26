import requests
from bs4 import BeautifulSoup

def scrape_data():
    url = 'https://gallica.bnf.fr/essentiels/tous-les-auteurs-toutes-les-oeuvres'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    livres = []
    for livre_element in soup.find_all('div', class_='col u-w33 item-list u-pad-r'):
        titre = livre_element.find('h4').text
        auteur_element = livre_element.find('div', class_='col u-w66')
        auteur = auteur_element.find('h3').text if auteur_element and auteur_element.find('h3') else "Auteur non trouvé"

        livres.append({'titre': titre, 'auteur': auteur})

    return livres
