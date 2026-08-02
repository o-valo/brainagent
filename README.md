# brainagent
### [ENG]  OpenAI-compatible Context Proxy combining SQL, vector search and plugins for LLMs. 

[Why the Brainagant was created. ](./brainagent-why.md).

###  [DEU] Brainagent ist ein OpenAI-kompatibler Context-Proxy für  LLMs. Er kombiniert SQL, Vektorsuche und Plugins, bevor eine Anfrage an das eigentliche Modell weitergeleitet wird.  

[Warum de rBrainagent entstanden ist. ](./de-brainagent-warum.md).

Anleitung: 
Brainagent: Installations- und Konfigurationsleitfaden
Der Brainagent fungiert als Middleware-Proxy, der Anfragen an LLMs (wie Ollama) durch eine Kombination aus relationaler SQL-Suche und Vektor-RAG (Retrieval-Augmented Generation) mit Kontext anreichert.
1. Vektordatenbank (Qdrant) einrichten
Die Vektordatenbank speichert Dokument-Chunks für die semantische Suche.

    Docker-Container starten: Verwende das Skript qdrant-start.docker.sh. Es startet Qdrant persistent als Daemon mit automatischem Neustart (--restart always).
    Collection anlegen: Führe qdrant-neuanlegen.sh aus. Dies erstellt die Collection docmost-rag mit 768 Dimensionen (passend für gängige Embedding-Modelle) und der Cosine-Metrik über die REST-API.
    Test der Suche: Mit simple-search.sh kannst du einen Testlauf direkt gegen die Qdrant-API unter http://xxx.xxx.xxx.xxx:6333 durchführen.

2. Relationales Backend (PostgreSQL) & Daten-Sync
Das SQL-Backend wird für den "SQL-First"-Ansatz genutzt, um exakte Fakten aus Metadaten zu priorisieren.

    Verbindungsparameter: In den Skripten müssen die Host-IP (xxx.xxx.xxx.xxx), der Datenbankname (rag_db), sowie User und Passwort hinterlegt werden.
    Initialer Datenimport: Das Skript sql-reset-import.py leert die Tabelle docmost_files und importiert alle Markdown-Dateien aus einem lokalen Verzeichnis (z. B. /mnt/data).
        Hinweis: Das Skript erzwingt die Prüfung der #EOF-Markierung am Ende jeder Datei.
    Integritätsprüfung: Nutze sql-health-check.py, um die Erreichbarkeit der Datenbank unter xxx.xxx.xxx.xxx und die Tabellenstruktur zu verifizieren.

3. RAG-Manager & Vektor-Indizierung
Nachdem die SQL-Daten vorhanden sind, müssen die Inhalte für die Vektorsuche aufbereitet werden.

    Indizierung: Starte rag_manager.py. Das Tool liest die Markdown-Dateien ein, erstellt überlappende Text-Chunks (um Informationsverlust an den Schnittstellen zu vermeiden) und lädt diese in Qdrant hoch.
    Status prüfen: Mit check-rag.py kannst du die Anzahl der erfolgreich indizierten Vektoren und den allgemeinen Status der Collection überwachen.

4. Brainagent Flask-Proxy starten
Dies ist die zentrale Komponente, die zwischen deinem Client (z. B. OpenWebUI) und dem LLM-Backend sitzt.

    Umgebungsvariablen: Setze die URL für dein Embedding-Modell (z. B. Ollama): export EMBEDDING_URL="http://xxx.xxx.xxx.xxx:11434".
    Server-Start: Starte den Proxy mit granit-brainagent.py (oder brainagent.py).
    Funktionsweise: Der Proxy nimmt Anfragen entgegen, führt zuerst eine SQL-Suche durch, ergänzt diese bei Bedarf um den Vektorkontext und leitet die finale Anfrage an das Backend weiter.

Übersicht der wichtigsten Werkzeuge im Repository
Alle Skripte sind darauf ausgelegt, die Integrität der Daten (z. B. durch #EOF-Prüfung) sicherzustellen:
Skript
	
Zweck
qdrant-start.docker.sh
	
Startet den Vektor-DB Container.
sql-reset-import.py
	
Synchronisiert Markdown-Files in PostgreSQL.
rag_manager.py
	
Erstellt Chunks und führt den Vektor-Upsert aus.
punkte-loeschen.sh
	
Ermöglicht das Löschen spezifischer IDs aus der Vektor-DB.
debug-log.py
	
Tool zur Fehlerdiagnose und Protokollierung.
Wichtig: Stelle sicher, dass die Ports für Qdrant (standardmäßig 6333) und PostgreSQL (standardmäßig 5432) auf den Ziel-IPs xxx.xxx.xxx.xxx für die Skripte erreichbar sind. #EOF







Powerd with ai :-)
