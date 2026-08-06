#!/usr/bin/env python3
# VERSION: 0.0.21
# STATUS: SQL-First Priorisierung + Query-Cleaning

import os
import time
import requests
import importlib.util
import re
from flask import Flask, request, jsonify

# Konfiguration (unverändert)
PROJECT_NAME = "Braintux"
VERSION = "0.0.21"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://xxx.xxx.xxx.xxx:11434") 
EMBEDDING_URL = os.getenv("EMBEDDING_URL", "http://xxx.xxx.xxx.xxx:11434") 
QDRANT_URL = os.getenv("QDRANT_URL", "http://xxx.xxx.xxx.xxx:6333")
EMBEDDING_MODEL = "nomic-embed-text-v2-moe"
SELECTED_MODEL = os.getenv("MODEL_NAME", "qwen3.5:9b-q8_0")
PORT = int(os.getenv("PROXY_PORT", 11435))
PLUGIN_FOLDER = "plugins"

DISABLED_PLUGINS = []

app = Flask(__name__)

def load_plugins():
    tools = {}
    if not os.path.exists(PLUGIN_FOLDER): return tools
    for fs_item in os.listdir(PLUGIN_FOLDER):
        if fs_item.endswith(".py"):
            name = fs_item[:-3]
            if name in DISABLED_PLUGINS: continue
            try:
                spec = importlib.util.spec_from_file_location(name, os.path.join(PLUGIN_FOLDER, fs_item))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "get_tool_definition") and hasattr(mod, "run"):
                    tools[name] = {"definition": mod.get_tool_definition(), "execute": mod.run}
                    print(f"[{time.strftime('%H:%M:%S')}] [PLUGINS] LOAD: {name}")
            except Exception as e:
                print(f"[{time.strftime('%H:%M:%S')}] [PLUGINS] FEHLER: {e}")
    return tools

plugins = load_plugins()

def clean_query_for_sql(text):
    """Entfernt Füllwörter, um die Volltextsuche nicht zu verwirren."""
    stop_phrases = [
        "suche nach", "wer ist", "wo wohnt", "finde info zu", 
        "zeig mir", "hast du infos über", "was ist"
    ]
    query = text.lower()
    for phrase in stop_phrases:
        query = query.replace(phrase, "")
    # Sonderzeichen entfernen, nur Wörter lassen
    query = re.sub(r'[^\w\s]', '', query).strip()
    return query

def is_internal_task(text):
    indicators = ["### Task:", "follow-up questions", "JSON format:", "<chat_history>"]
    return any(ind in text for ind in indicators)

def get_rag_context(query):
    try:
        emb = requests.post(f"{EMBEDDING_URL}/api/embeddings", 
                            json={"model": EMBEDDING_MODEL, "prompt": query}, timeout=20).json()
        vector = emb.get("embedding")
        res = requests.post(f"{QDRANT_URL}/collections/docmost-rag/points/search", 
                            json={"vector": vector, "limit": 3, "with_payload": True}, timeout=20)
        hits = res.json().get("result", [])
        return "\n".join([h.get("payload", {}).get("text", "") for h in hits if h.get("payload", {}).get("text")])
    except Exception: return ""

@app.route('/v1/chat/completions', methods=['POST'])
@app.route('/chat/completions', methods=['POST'])
def proxy_completions():
    try:
        data = request.get_json()
        data["model"] = SELECTED_MODEL
        data["stream"] = False
        messages = data.get("messages", [])

        if messages and messages[-1]["role"] == "user":
            user_query = messages[-1]["content"]
            
            if not is_internal_task(user_query):
                # 1. SQL-SUCHE ZUERST (Bereinigt)
                sql_context = ""
                if "pg_lookup" in plugins:
                    search_term = clean_query_for_sql(user_query)
                    print(f"[{time.strftime('%H:%M:%S')}] [SQL-FIRST] Suche nach: '{search_term}'")
                    sql_context = plugins["pg_lookup"]["execute"](search_term)

                # 2. RAG-SUCHE DANACH
                rag_context = get_rag_context(user_query)
                
                # Konstruktion des Kontext-Blocks (SQL oben!)
                combined = ""
                if sql_context and "Keine Treffer" not in sql_context:
                    combined += f"CRITICAL FACTS (POSTGRES):\n{sql_context}\n\n"
                
                if rag_context:
                    combined += f"ADDITIONAL CONTEXT (VECTOR):\n{rag_context}\n"

                if combined:
                    messages[-1]["content"] = f"Kontext:\n{combined}\n\nFrage: {user_query}"

        data["messages"] = messages
        resp = requests.post(f"{OLLAMA_URL}/v1/chat/completions", json=data, timeout=600)
        return jsonify(resp.json()), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e), "v": VERSION}), 500

# OpenWebUI Endpunkte (unverändert)
@app.route('/v1/models', methods=['GET'])
def list_models():
    return jsonify({"object": "list", "data": [{"id": SELECTED_MODEL, "object": "model", "created": int(time.time()), "owned_by": PROJECT_NAME}]})

@app.route('/api/tags', methods=['GET'])
def fake_tags(): return jsonify({"models": [{"name": SELECTED_MODEL, "model": SELECTED_MODEL}]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
# powerd with ai :-)
#EOF
