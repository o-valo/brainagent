#!/usr/bin/env python3
# VERSION: 0.1.3
# LAST_UPDATE: 2026-05-08
# DESCRIPTION: Löscht alle SQL-Daten und importiert neu aus /mnt/data

import os
import psycopg2
import time

# --- KONFIGURATION ---
DB_CONFIG = {
    "host": "192.168.2.42",
    "database": "rag_db",
    "user": "rag",
    "password": "rag"
}

DOCS_PATH = "/mnt/data"

def run_reset_and_import():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print(f"--- RESET: Lösche alte Daten in docmost_files ---")
        cur.execute("TRUNCATE TABLE docmost_files;")
        conn.commit()
        print("Datenbank ist jetzt leer.")

        print(f"\n--- START NEUIMPORT: {DOCS_PATH} ---")
        
        files = [f for f in os.listdir(DOCS_PATH) if f.endswith(".md")]
        total = len(files)
        added = 0
        
        for filename in files:
            path = os.path.join(DOCS_PATH, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                
                if not content:
                    continue

                # #EOF Regel erzwingen
                if not content.endswith("#EOF"):
                    content += "\n\n#EOF"

                cur.execute("""
                    INSERT INTO docmost_files (filename, content, indexed_at)
                    VALUES (%s, %s, CURRENT_TIMESTAMP);
                """, (filename, content))
                added += 1
                
                if added % 20 == 0:
                    print(f"Fortschritt: {added}/{total} Dateien...")

            except Exception as file_err:
                print(f"Fehler bei {filename}: {file_err}")

        conn.commit()
        print(f"\n--- ERFOLG ---")
        print(f"Dateien im Verzeichnis: {total}")
        print(f"Neu angelegt in SQL:   {added}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Kritischer Fehler: {e}")

if __name__ == "__main__":
    run_reset_and_import()

#EOF
