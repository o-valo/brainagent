# brainagent
### [ENG]  OpenAI-compatible Context Proxy combining SQL, vector search and plugins for LLMs. 

[Why the Brainagant was created. ](./brainagent-why.md).

##  1. Setting up the Vector Database (Qdrant)
The vector database is responsible for semantic search across your document chunks.

    Start the Container: Use the script qdrant-start.docker.sh to launch Qdrant as a persistent Docker container with an automatic restart policy (--restart always).
    Create the Collection: Run qdrant-neuanlegen.sh to initialize the docmost-rag collection. This is pre-configured with 768 dimensions and the Cosine metric, matching standard embedding models.
    Verify Connectivity: You can test the Qdrant API at http://xxx.xxx.xxx.xxx:6333 using simple-search.sh to perform a test query.

2. Relational Backend (PostgreSQL) & Data Sync
The PostgreSQL database handles the "SQL-First" logic to ensure exact fact-finding from metadata.

    Configuration: Ensure your scripts are pointed to your database host at xxx.xxx.xxx.xxx. The default setup expects a database named rag_db.
    Initial Data Import: Use sql-reset-import.py to clear the docmost_files table and synchronize Markdown files from your source directory (e.g., /mnt/data). This script strictly enforces the #EOF marker rule for all imported files.
    Health Check: Run sql-health-check.py to confirm the database at xxx.xxx.xxx.xxx is reachable and the table structures are correct.

3. RAG Pipeline & Vector Indexing
Once the metadata is in the SQL database, you must index the content for semantic retrieval.

    Indexing Documents: Execute rag_manager.py. This script reads the Markdown files, creates overlapping text chunks (to prevent information loss at boundaries), and performs a vector upsert into Qdrant.
    Monitor Status: Use check-rag.py to verify the total count of indexed vectors and ensure the collection status is healthy.

4. Starting the Brainagent Flask Proxy
This is the core middleware component that processes incoming requests.

    Environment Setup: Before starting, export the URL for your embedding model (e.g., your Ollama instance): export EMBEDDING_URL="http://xxx.xxx.xxx.xxx:11434".
    Start the Server: Launch the proxy using granit-brainagent.py (or brainagent.py as found in the repository).
    How it Works: The proxy receives a request, executes a cleaned SQL search first, enriches it with RAG context if needed, and then forwards the augmented prompt to the LLM.

Overview of Key Scripts
All scripts are designed to maintain data integrity through automated checks:
Script
	
Purpose
qdrant-start.docker.sh
	
Launches the Qdrant vector database container.
sql-reset-import.py
	
Syncs Markdown files to PostgreSQL with #EOF validation.
rag_manager.py
	
Handles chunking and vector upserts into Qdrant.
punkte-loeschen.sh
	
Deletes specific vector points (IDs) from the collection.
debug-log.py
	
Provides diagnostics and protocol logging.
Note: Ensure that ports 6333 (Qdrant) and 5432 (PostgreSQL) are open and accessible at your specified IP xxx.xxx.xxx.xxx for these scripts to function correctly. #EOF



###  [DEU] Brainagent ist ein OpenAI-kompatibler Context-Proxy für  LLMs. Er kombiniert SQL, Vektorsuche und Plugins, bevor eine Anfrage an das eigentliche Modell weitergeleitet wird.  

[Warum de rBrainagent entstanden ist. ](./de-brainagent-warum.md).

## Anleitung: 
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
