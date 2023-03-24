from pythonping import ping
from colorama import Fore
from pystyle import *
import os
import re
import ipaddress 
import requests
import time
import whois
import socket
from bs4 import BeautifulSoup
import json


# Fonction pour récupérer l'adresse IP d'un site web
def recup_ip():
    print()
    hostname = input("Entrer l'url du site : ").replace("https://", "")
    print()

    try:
        ip_address = socket.gethostbyname(hostname)
        print(f"L'adresse IP de {hostname} est {ip_address}")
    except socket.gaierror:
        print(f"Impossible de récupérer l'adresse IP pour {hostname}. Veuillez vérifier l'URL et réessayer.")
        
    time.sleep(5)


# Fonction pour extraire toutes les adresses email d'une page web
def extract_all_emails_from_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    emails = []
    for tag in soup.find_all(string=email_regex):
        found_emails = re.findall(email_regex, tag)
        for email in found_emails:
            if not email.endswith(('wixpress.com', 'atos.net', 'sentry.io')) and email not in emails:
                emails.append(email)
    return emails


def mail():
    while True:
        url = input("url ? : ")
        if not url.startswith("http://") and not url.startswith("https://"):
            print("L'URL doit commencer par http:// ou https://")
        else:
            break

    try:
        emails = extract_all_emails_from_webpage(url)
        if emails:
            print("Adresses email trouvées : ", url,":")
            with open('emails.txt', 'a') as email_file:
                for email in emails:
                    print(" -", email)
                    email_file.write(email + '\n')
        else:
            print("Aucune adresse email trouvée sur", url)
            contact_url = url + "contact/"
            emails = extract_all_emails_from_webpage(contact_url)
            if emails:
                print("Adresses email trouvées sur", contact_url, ":")
                with open('emails.txt', 'a') as email_file:
                    for email in emails:
                        print(" -", email)
                        email_file.write(email + '\n')
            else:
                print("Aucune adresse email trouvée sur", contact_url)
    except (requests.exceptions.SSLError, requests.exceptions.RequestException):
        print("Erreur lors de la récupération de la page", url)
        return []
    
    time.sleep(5)
    print()
    



# Fonction pour récupérer des informations sur un nom de domaine3

def get_domain_info():
    print()
    domain_name = input('Nom de domaine/IP : ')
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
        if whois_info.status:
            info_dict["Status"] = whois_info.status
        if whois_info.name:
            info_dict["Nom du propriétaire"] = whois_info.name
        if whois_info.emails:
            info_dict["Emails du propriétaire"] = whois_info.emails
        if whois_info.address:
            info_dict["Adresse du propriétaire"] = whois_info.address
        if whois_info.city:
            info_dict["Ville du propriétaire"] = whois_info.city
        if whois_info.state:
            info_dict["Etat/province du propriétaire"] = whois_info.state
        if whois_info.country:
            info_dict["Pays du propriétaire"] = whois_info.country
        if whois_info.name_servers:
            info_dict["Serveurs de noms"] = whois_info.name_servers
        if info_dict:
            print("Informations WHOIS pour", domain_name + ":")
            for key, value in info_dict.items():
                print(key + ":", value)
        else:
            print("Aucune information WHOIS trouvée pour", domain_name)

    except Exception as e:
        print("Erreur : ", e)
        print("Impossible de récupérer les informations WHOIS pour", domain_name)
    
    time.sleep(5)
    print()
    


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

    time.sleep(5)
    print()
    


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

        filename = f"CVE-{ip_address}.txt"
        with open(filename, "w") as f:
            f.write(content)
        print(f"Les CVE ont été enregistrées dans le fichier {filename}")
    else:
        print(f"Aucunes CVE détectées {ip_address}")

    time.sleep(5)
    print()
    


# Fonction pour ping une ip
def ping_ip():
    print()
    while True:
        ip_addr = input('Entrer une IP : ')
        if is_valid_ip_address(ip_addr) and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_addr):
            break
        else:
            print(f"{ip_addr} n'est pas une adresse IP valide. Veuillez entrer une adresse IP valide.")
            continue
    print()

    ping_result = ping(ip_addr, verbose=True)

    if ping_result.success:
        print()
    else:
        print("Aucun ping possible.")

    time.sleep(5)
    print()

def menu():
    while True:
        print((Colorate.Vertical(Colors.green_to_cyan,"""
            ██╗██████╗     ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗ 
            ██║██╔══██╗    ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗
            ██║██████╔╝    ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝
            ██║██╔═══╝     ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗
            ██║██║         ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║
            ╚═╝╚═╝         ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
        """)))
        print(Colorate.Vertical(Colors.blue_to_green,"""
                ╔════════════════════════════════════════════════════╗
                ║                        Menu                        ║
                ╠════════════════════════════════════════════════════╣
                ║                                                    ║
                ║ 1. Connaître l'adresse IP d'un site                ║
                ║ 2. Rechercher des adresses e-mail sur un site      ║
                ║ 3. Whois                                           ║
                ║ 4. Scan de port                                    ║
                ║ 5. Recherche de CVE                                ║
                ║ 6. Ping IP                                         ║
                ║ 7. Quitter                                         ║
                ║                                                    ║
                ╠════════════════════════════════════════════════════╣
                ║               Développé par M3gac0rp               ║
                ╚════════════════════════════════════════════════════╝        
        
        """))

        choix = input("Entrez votre choix : ")
        print("")
        
        try:
            choix = int(choix)
        except ValueError:
            print("Choix invalide. Veuillez réessayer.")
            time.sleep(3)
            os.system('cls')
            continue

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
