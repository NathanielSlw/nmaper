#!/usr/bin/env python3

import sys
import subprocess
import re
import os

# Terminal colors
RESET = "\033[0m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"

# Help message
usage = f"""{YELLOW}Usage:
    nmaper IP/FILE [OPTIONS]

OPTIONS:
    ALL     : Scan all ports (-p-)
    (all other valid Nmap options are also accepted directly)
    -h, --help : Show this help message{RESET}

Example:
    - Scan a single target with the default quick and in-depth scan
        nmaper.py 192.168.1.1

    - Scan all ports of a target (-p-)
        nmaper.py 192.168.1.1 ALL

    - Use custom Nmap options (e.g. fast UDP scan)
        nmaper.py 192.168.1.1 -sU -T4

    - Scan multiple targets listed in a file
        nmaper.py targets.txt
"""

# Argument check
if len(sys.argv) == 1:
    print(usage)
    sys.exit(1)

# Help option
if sys.argv[1] in ("-h", "--help"):
    print(usage)
    sys.exit(0)

# Main parameter (target or file)
TARGET = sys.argv[1]
ALL_PORTS = '-p-'

# Available options
OPTIONS = {
    "ALL": [ALL_PORTS]
}

# Collect selected options
selected_options = []
for arg in sys.argv[2:]:
    if arg in OPTIONS:
        selected_options.extend(OPTIONS[arg])
    else:
        selected_options.append(arg)

def scan_target(target):
    """
    Runs an Nmap scan on a given target in 2 steps:
    - Step 1: quick scan to detect open ports
    - Step 2: in-depth scan with -A on detected ports
    """

    print(f"{YELLOW}[+] Scan de la cible : {target}{RESET}")

    # Base command for the first step
    nmap_parameters = ['nmap', target, '-Pn', '--open'] + selected_options

    # Filename adapted to the target
    safe_target = target.replace('/', '_').replace(':', '_')
    filename = f"nmap_{safe_target}.txt"
    if "-p-" in nmap_parameters:
        filename = f"nmap_all_{safe_target}.txt"

    # Step 1: detect open ports ---------------------------------------------------------------
    print(f"{YELLOW}[+] Étape 1 : Détection des ports ouverts...{RESET}")
    nmap_result = subprocess.run(nmap_parameters, stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(nmap_result)

    # Extract open ports (lines starting with a digit)
    regex = r"^\d+.*$"
    res = re.findall(regex, nmap_result, re.MULTILINE)

    ports = []
    if res:
        for portline in res:
            ports.append(portline.split("/")[0])

        # Remove '-p-' to avoid rescanning all ports in step 2
        if "-p-" in nmap_parameters:
            nmap_parameters.remove("-p-")

        # Step 2: advanced scan on open ports ---------------------------------------------------------------
        print(f"\n{YELLOW}[+] Étape 2 : Scan avancé avec détection service et OS (-A)...{RESET}")
        nmap_parameters.extend(['-p', ",".join(ports), '-A', '-oN', filename])
        nmap_result = subprocess.run(nmap_parameters, stdout=subprocess.PIPE).stdout.decode('utf-8')
        print(nmap_result)
        print(f"{BLUE}[+] Résultat sauvegardé dans : {filename}{RESET}\n")
    else:
        print(f"{RED}[-] Aucun port ouvert détecté. Scan approfondi annulé pour {target}.{RESET}\n")

# === Main ===
if os.path.isfile(TARGET):
    # If a file is provided, read targets from it
    with open(TARGET, 'r') as f:
        targets = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    print(f"{GREEN}[+] {len(targets)} cibles détectées dans le fichier.{RESET}\n")
    for tgt in targets:
        scan_target(tgt)
else:
    # Otherwise, scan a single target
    scan_target(TARGET)
