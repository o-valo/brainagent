#!/usr/bin/env python3
"""
rag_manager.py - Version 0.0.4
Funktion: Überlappende Chunks (Overlap), um Informationsverlust zu verhindern.
"""

import os
import hashlib
import time
import requests
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Konfiguration
SOURCE_DIR = "/mnt/data"
QDRANT_URL = "http://10.7.0.99:6333"
COLLECTION_NAME = "docmost-rag"
OLLAMA_URL = "http://192.168.2.76:11434"
MODEL = "nomic-embed-text-v2-moe:latest"
CHUNK_SIZE = 1200
OVERLAP = 200

client = QdrantClient(url=QDRANT_URL)

def get_chunk_id(filename, start_index):
    # Eindeutige ID basierend auf Datei und Position
    raw_id = f"{filename}_{start_index}"
    return int(hashlib.md5(raw_id.encode()).hexdigest(), 16) % 1000000000

def run():
    print(f"--- RAG Manager v0.0.4 (Overlap: {OVERLAP}) ---")
    files = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".md")]
    
    for filename in files:
        path = os.path.join(SOURCE_DIR, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Erstelle überlappende Chunks
        for i in range(0, len(content), CHUNK_SIZE - OVERLAP):
            chunk = content[i:i + CHUNK_SIZE]
            
            # Embedding abrufen
            r = requests.post(f"{OLLAMA_URL}/api/embeddings", 
                              json={"model": MODEL, "prompt": chunk})
            
            if r.status_code != 200:
                continue

            data = r.json()
            
            # Upsert
            client.upsert(
                collection_name=COLLECTION_NAME,
                points=[models.PointStruct(
                    id=get_chunk_id(filename, i), 
                    vector=data["embedding"], 
                    payload={"filename": filename, "text": chunk} 
                )]
            )
            print(f"ERFOLG: {filename} Chunk ab {i} indiziert.")
            
            if len(chunk) < CHUNK_SIZE: break # Ende der Datei erreicht

if __name__ == "__main__":
    run()

#EOF
