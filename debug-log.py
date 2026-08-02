#!/usr/bin/env python3
"""
rag_manager.py - Version 0.0.6
Debug: Prüft aktiv auf das Vorhandensein der Adresse beim Einlesen.
"""

import os
import hashlib
import requests
import logging

# Konfiguration
SOURCE_DIR = "/mnt/data"
LOG_FILE = "rag_manager.log"
OLLAMA_URL = "http://192.168.2.76:11434"
MODEL = "nomic-embed-text-v2-moe:latest"

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

def run():
    print(f"--- RAG Manager v0.0.6 (Debug-Mode aktiv) ---")
    
    for filename in os.listdir(SOURCE_DIR):
        if not filename.endswith(".md"): continue
        
        path = os.path.join(SOURCE_DIR, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # DEBUG: Konsole-Check
        if "Neuchateller" in content:
            print(f"!!! GEFUNDEN !!! 'Neuchateller' wurde in {filename} erkannt.")
        else:
            print(f"Suche... 'Neuchateller' nicht in {filename} gefunden.")
            
        # Hier würde nun die Indizierung wie gewohnt weitergehen...
        # ... (restlicher Code bleibt gleich)

if __name__ == "__main__":
    run()
#EOF
