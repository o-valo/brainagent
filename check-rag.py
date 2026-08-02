#!/usr/bin/env python3
"""
check-rag.py - Analyse der Datenbank-Integrität
"""

from qdrant_client import QdrantClient

# --- KONFIGURATION ---
QDRANT_URL = "http://10.7.0.99:6333"
COLLECTION_NAME = "docmost-rag"

def check_db():
    try:
        client = QdrantClient(url=QDRANT_URL)
        
        # 1. Anzahl der Vektoren prüfen
        count = client.count(collection_name=COLLECTION_NAME, exact=True)
        print(f"=== Datenbank-Analyse: {COLLECTION_NAME} ===")
        print(f"Gesamtzahl der Vektoren: {count.count}")
        
        # 2. Status der Collection (inkl. Speichergröße)
        info = client.get_collection(collection_name=COLLECTION_NAME)
        # Qdrant gibt die geschätzte Größe in Bytes aus
        size_bytes = info.payload_schema.get('size_bytes', 'Nicht direkt verfügbar')
        print(f"Collection Status: {info.status}")
        
        # 3. Stichprobe (letzte 10)
        print("\n--- Stichprobe (letzte 10 Einträge) ---")
        points, _ = client.scroll(
            collection_name=COLLECTION_NAME, 
            limit=10, 
            with_payload=True
        )
        
        for p in points:
            print(f"ID: {p.id} | Datei: {p.payload.get('filename')}")
            
    except Exception as e:
        print(f"Fehler bei der Abfrage: {e}")

if __name__ == "__main__":
    check_db()

#EOF
