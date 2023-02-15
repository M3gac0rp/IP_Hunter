from pythonping import ping
import re
import requests
import whois
from bs4 import BeautifulSoup
import json


def ping_ip():
    ip_addr = input('Enter the IP address : ')

    ping_result = ping(ip_addr, verbose=True)

    if ping_result.success:
        print()
    else:
        print("Aucun ping possible.")

#ping_ip()

def extract_all_emails_from_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = []
    for tag in soup.find_all(string=email_regex):
        emails += re.findall(email_regex, tag)
    return emails

def mail():
    url = input("url ?  ")
    emails = extract_all_emails_from_webpage(url)
    if emails:
        print("Adresses email trouvées :")
        for email in emails:
            print(" -", email)
    else:
        print("Aucune adresse email trouvée")

    with open('emails.txt', 'a') as email_file:
        for email in emails:
            if 'wixpress.com' not in email:
                email_file.write(email + '\n')

#mail()



def get_domain_info():
    domain_name = input('Nom de domaine/ip : ')
    try:
        whois_info = whois.whois(domain_name)
        info_dict = {}
        if whois_info.registrar:
            info_dict["Registrar"] = whois_info.registrar
        if whois_info.whois_server:
            info_dict["WHOIS server"] = whois_info.whois_server
        if whois_info.creation_date:
            info_dict["Creation date"] = str(whois_info.creation_date)
        if whois_info.expiration_date:
            info_dict["Expiration date"] = str(whois_info.expiration_date)
    except Exception as e:
        print("Error: ", e)
    print(whois_info)

#get_domain_info(domain_name)


def port():
    # Adresse IP à rechercher
    ip_address = input('Entrer une adresse ip : ')

    # URL de la page de résultats de recherche pour l'adresse IP
    url = f'https://www.shodan.io/host/{ip_address}'

    # Récupérer la page HTML
    response = requests.get(url)

    # Charger la page HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver l'élément avec l'ID "ports"
    element_id = "ports"
    elements = soup.find(id=element_id)

    if elements:
        content = ", ".join([element.text.strip() for element in elements])
        print(f"Ports ouverts pour l'adresse IP {ip_address}: {content}")
    else:
        print(f"Aucun port ouvert pour l'adresse IP {ip_address}")

#port()


def cve():
    # Adresse IP à rechercher
    ip_address = input('Entrer une adresse ip : ')

    # URL de la page de résultats de recherche pour l'adresse IP
    url = f'https://www.shodan.io/host/{ip_address}'

    # Récupérer la page HTML
    response = requests.get(url)

    # Charger la page HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Trouver l'élément avec l'ID "ports"
    element_id = "vulnerabilities"
    elements = soup.find(id=element_id)

    if elements:
        content = ", ".join([element.text.strip() for element in elements])
        print(f"{content}")
    else:
        print(f"Aucunes CVE détectées {ip_address}")


cve()




