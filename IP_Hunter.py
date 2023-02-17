from pythonping import ping
import os
import re
import ipaddress 
import requests
import whois
import socket
from bs4 import BeautifulSoup
import json


# Fonction pour récupérer l'adresse IP d'un site web
def recup_ip():
    print()
    hostname = input("Entrer l'url du site : ").replace("https://", "")
    print()

    ip_address = socket.gethostbyname(hostname)
    print()
    print(f"L'adresse IP de {hostname} est {ip_address}")
    print()


# Fonction pour extraire toutes les adresses email d'une page web
def extract_all_emails_from_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = []
    for tag in soup.find_all(string=email_regex):
        emails += re.findall(email_regex, tag)
    return emails


# Fonction pour récupérer toutes les adresses email d'une page web et les écrire dans un fichier "emails.txt"
def mail():
    print()
    while True:
        url = input("url ? : ")
        print()
        if not url.startswith("http://") and not url.startswith("https://"):
            print("L'URL doit commencer par http:// ou https://")
            print()
        else:
            break
    
    try:
        emails = extract_all_emails_from_webpage(url)
    except requests.exceptions.RequestException as e:
        print(f"Impossible de récupérer les emails : {e}")
        return

    if emails:
        print("Adresses email trouvées : ")
        for email in emails:
            print(" -", email)
    else:
        print("Aucune adresse email trouvée")

    with open('emails.txt', 'a') as email_file:
        for email in emails:
            if 'wixpress.com' not in email:
                email_file.write(email + '\n')


# Fonction pour récupérer des informations sur un nom de domaine
def get_domain_info():
    print()
    domain_name = input('Nom de domaine/ip : ')
    print()

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



def is_valid_ip_address(ip_address):
    try:
        socket.inet_aton(ip_address)
        return True
    except socket.error:
        return False


# Fonction pour récupérer les ouverts
def port():
    # Adresse IP à rechercher
    print()
    while True:
        ip_address = input('Entrer une IP : ')
        if is_valid_ip_address(ip_address):
            break
        else:
            print(f"{ip_address} n'est pas une adresse IP valide. Veuillez entrer une adresse IP valide.")
    print()

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
        print(f"Ports ouverts pour l'adresse IP {ip_address} : {content}")
    else:
        print(f"Aucun port ouvert pour l'adresse IP {ip_address}")


# Fonction pour rechercher les CVEs  
def cve():
    # Adresse IP à rechercher
    while True:
        ip_address = input('Entrer une IP : ')
        if is_valid_ip_address(ip_address):
            break
        else:
            print(f"{ip_address} n'est pas une adresse IP valide. Veuillez entrer une adresse IP valide.")
    print()

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


# Fonction pour ping une ip
def ping_ip():
    print()
    while True:
        ip_addr = input('Entrer une IP : ')
        if is_valid_ip_address(ip_addr):
            break
        else:
            print(f"{ip_addr} n'est pas une adresse IP valide. Veuillez entrer une adresse IP valide.")
    print()

    ping_result = ping(ip_addr, verbose=True)

    if ping_result.success:
        print()
    else:
        print("Aucun ping possible.")

def menu():
    while True:
        print()
        print()
        print("██╗██████╗     ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ ")
        print("██║██╔══██╗    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗")
        print("██║██████╔╝    ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝")
        print("██║██╔═══╝     ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗")
        print("██║██║         ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║")
        print("╚═╝╚═╝         ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝")
        print()
        print("╔════════════════════════════════════════════════════╗")
        print("║                        Menu                        ║")
        print("╠════════════════════════════════════════════════════╣")
        print("║                                                    ║")
        print("║ 1. Connaître l'adresse IP d'un site                ║")
        print("║ 2. Rechercher des adresses e-mail sur un site      ║")
        print("║ 3. Whois                                           ║")
        print("║ 4. Scan de port                                    ║")
        print("║ 5. Recherche de CVE                                ║")
        print("║ 6. Ping IP                                         ║")
        print("║ 7. Quitter                                         ║")
        print("║                                                    ║")
        print("╠════════════════════════════════════════════════════╣")
        print("║               Développé par M3gac0rp               ║")
        print("╚════════════════════════════════════════════════════╝")        
        print("")


        choix = int(input("Entrez votre choix : "))
        print("")


        if choix == 1:
            recup_ip()
        elif choix == 2:
            mail()
        elif choix == 3:
            get_domain_info()
        elif choix == 4:
            port()
        elif choix == 5:
            cve()
        elif choix == 6:
            ping_ip()
        elif choix == 7:
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")
os.system('cls')
menu()