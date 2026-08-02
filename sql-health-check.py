#!/usr/bin/env python3
# VERSION: 0.1.0
# DESCRIPTION: Checkt den Inhalt der rag_db auf .42

import psycopg2
from tabulate import tabulate # Falls nicht installiert: pip install tabulate

DB_CONFIG = {
    "host": "192.168.2.42",
    "database": "rag_db",
    "user": "rag",
    "password": "rag"
}

def check_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # 1. Welche Tabellen gibt es überhaupt?
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cur.fetchall()
        print(f"--- Vorhandene Tabellen ---")
        for t in tables:
            print(f" - {t[0]}")
        
        # 2. Wie viele Einträge sind in docmost_files?
        cur.execute("SELECT COUNT(*) FROM docmost_files")
        count = cur.fetchone()[0]
        print(f"\nAnzahl der Dateien in 'docmost_files': {count}")
        
        # 3. Die 5 neuesten Einträge zeigen
        if count > 0:
            print(f"\n--- Die 5 neuesten Einträge ---")
            cur.execute("""
                SELECT filename, length(content) as size, indexed_at 
                FROM docmost_files 
                ORDER BY indexed_at DESC 
                LIMIT 5
            """)
            rows = cur.fetchall()
            print(tabulate(rows, headers=['Dateiname', 'Größe (Chars)', 'Zeitstempel']))

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Fehler beim DB-Check: {e}")

if __name__ == "__main__":
    check_db()

#EOF
