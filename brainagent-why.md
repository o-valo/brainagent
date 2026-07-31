#  [ENG] The Story of the Brainagent

In the beginning, I didn't plan on developing a "Brainagent" at all. I simply wanted to learn how the mechanisms behind an AI work—locally with Ollama, not in the cloud. I quickly noticed that small models hallucinate constantly.

Then I read about RAG (Retrieval-Augmented Generation). This method was supposed to solve precisely that problem. My first attempts were promising; I tried Flowise, a framework for creating RAG systems.

However, that turned out to be a dead end. Flowise kept crashing. Dify also looked promising at first, but proved to be too complex. What I was actually looking for was a very simple solution—just a mechanism to export my DocMost data. Implementing that took me a full day.

Since I had now tested two frameworks and was satisfied with neither, I installed a vector database and imported my DocMost export. Open WebUI could process RAG systems—so I thought I would connect my vector database directly there. After about five hours, I realized: that didn't work at all as hoped.

Before that, however, I had already built various small miniproxies using AI coding tools, and they worked flawlessly. So what could be more natural than building my own proxy to connect my vector database to Open WebUI? With that, the idea of the "Brainagent" was born.
Why Brainagent: The AI with a "Fact Memory"

My Brainagent is basically an intelligent mediator—a proxy that sits right between the user interface and the local AI model. The clever part: the AI isn't allowed to just guess at random. Before it gives an answer, it first has to look things up in two different archives.
First, the "Fact Check" comes into action

A special Postgres plugin—imagine a digital filing cabinet containing hard data like IP addresses or hardware lists. The system uses intelligent full-text search and evaluates which match fits the question best. So if I ask for the IP address of my SSH server, the agent finds the exact number in the files instead of guessing.
Next comes the "Meaning Search" in the RAG archive

This is where hundreds of documents reside, sorted by their meaning. The AI searches there for passages that match the question in content—even if the words don't match one-to-one. This is like an assistant copying the most relevant pages and handing them to the AI as a cheat sheet.
The "Cleaning Crew": Query Cleaning

To ensure the search works cleanly in the first place, I built in a filter. The system radically processes the user's question: a polite "Could you please pull the info on the IPs for me?" simply becomes "Server IPs". This way, the database isn't distracted by smalltalk and delivers much more precise results.
The "Law of Honesty"

The most important thing is strict source binding. The AI is coupled to the info from the SQL fact check and the RAG archive with clear instructions: "Only use what is in black and white right here!" If the system finds nothing in the databases, the AI is not allowed to invent anything. It sticks to the truth and does not hallucinate.

In the end, I have exactly what I wanted: absolute privacy (everything runs locally), extremely high precision, and a modular system where I can swap out the AI brain at any time without losing my knowledge archive.
The Architecture: Down to Brass Tacks

    Main model: Granite 4.1 8B – Final answer generation

    Worker model: nomic-embed-text-v2-moe – Optimized for embeddings

    Vector store: Qdrant vector database – Fast meaning search

    Fact store: PostgreSQL server – Exact data inventories

    Interface: 2× Ollama – Local runtime environment

#EOF
