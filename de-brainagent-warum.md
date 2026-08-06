#  [DEU] Die Geschichte des Braintux

Am Anfang hatte ich noch gar nicht vor, einen „Braintux" zu entwickeln. Ich wollte lediglich lernen, wie die Mechanismen hinter einer KI funktionieren – lokal mit Ollama, nicht in der Cloud. Dabei merkte ich schnell: kleine Modelle halluzinieren ständig.

Dann las ich über RAG (Retrieval-Augmented Generation). Das Verfahren sollte genau das Problem lösen. Meine ersten Versuche waren vielversprechend; ich probierte Flowise aus, ein Framework zur Erstellung von RAG-Systemen.

Das erwies sich jedoch als Sackgasse. Flowise stürzte ständig ab. Auch Dify war zunächst vielversprechend, erwies sich aber als zu komplex. Ich suchte eigentlich nach einer sehr einfachen Lösung – nur einen Mechanismus zum Exportieren meiner DocMost-Daten. Die Umsetzung hat mich einen kompletten Tag gekostet.

Da ich nun zwei Frameworks getestet hatte und mit beiden nicht zufrieden war, installierte ich mir eine Vektordatenbank und importierte meinen DocMost-Export. Open WebUI konnte RAG-Systeme verarbeiten – also dachte ich, ich schließe meine Vektordatenbank direkt dort an. Nach etwa fünf Stunden stellte ich fest: Das funktionierte überhaupt nicht wie erhofft.

Zuvor hatte ich mir jedoch bereits verschiedene kleine Miniproxies mithilfe von KI-Coding-Tools gebaut, und diese funktionierten einwandfrei. Was lag also näher, als einen eigenen Proxy zu bauen, um meine Vektordatenbank an Open WebUI anzubinden? Damit war die Idee des „Braintux" geboren.

---

## Warum Braintux: Die KI mit dem „Fakten-Gedächtnis"

Mein Braintux ist im Grunde ein intelligenter Vermittler – ein Proxy, der genau zwischen der Benutzeroberfläche und dem lokalen KI-Modell sitzt. Der Clou: Die KI darf nicht einfach drauf los raten. Bevor sie eine Antwort gibt, muss sie erst in zwei verschiedenen Archiven nachschlagen.

### Zuerst tritt der „Fakten-Check" in Aktion

Ein spezielles Postgres-Plugin – stellen Sie sich einen digitalen Aktenschrank vor, in dem knallharte Daten wie IP-Adressen oder Hardware-Listen stehen. Das System nutzt intelligente Volltextsuche und bewertet, welcher Treffer am besten zur Frage passt. Wenn ich also nach der IP-Adresse meines SSH-Servers frage, findet der Agent die exakte Zahl in den Akten, anstatt zu schätzen.

### Dann geht es an die „Sinn-Suche" im RAG-Archiv

Hier liegen hunderte Dokumente, sortiert nach ihrer Bedeutung. Die KI sucht dort nach Stellen, die inhaltlich zur Frage passen – selbst wenn die Wörter nicht eins zu eins übereinstimmen. Das ist wie ein Assistent, der die relevantesten Seiten kopiert und der KI als Spickzettel hinlegt.

### Die „Putzkolonne": Query-Cleaning

Damit die Suche aber überhaupt sauber funktioniert, habe ich einen Filter eingebaut. Das System bearbeitet die Nutzerfrage radikal: Aus einem höflichen „Könntest du mir bitte mal die Infos zu den IPs raussuchen?" wird einfach nur „Server-IPs". So wird die Datenbank nicht durch Smalltalk abgelenkt und liefert viel präzisere Ergebnisse.

### Das „Ehrlichkeit-Gesetz"

Das Wichtigste ist die strikte Quellenbindung. Die KI ist an die Infos aus dem SQL-Fakten-Check und dem RAG-Archiv gekoppelt und hat die klare Anweisung: „Nutze nur das, was hier schwarz auf weiß steht!" Wenn das System in den Datenbanken nichts findet, darf die KI nichts erfinden. Sie bleibt bei der Wahrheit und halluziniert nicht.

Am Ende habe ich genau das, was ich wollte: **absolute Privatsphäre** (alles läuft lokal), **extrem hohe Präzision** und ein **modulares System**, bei dem ich das KI-Gehirn jederzeit tauschen kann, ohne mein Wissens-Archiv zu verlieren.

---

## Die Architektur: Butter bei die Fische

- **Hauptmodell**: Granite 4.1 8B – Finale Antwortgenerierung
- **Worker-Modell**: nomic-embed-text-v2-moe – Optimiert für Embeddings
- **Vektorspeicher**: Qdrant Vektordatenbank – Schnelle Sinn-Suche
- **Faktenspeicher**: PostgreSQL Server – Exakte Datenbestände
- **Schnittstelle**: 2× Ollama – Lokale Laufzeitumgebung
