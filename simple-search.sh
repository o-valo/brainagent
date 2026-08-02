#!/bin/sh



curl -X POST 'http://10.7.0.99:6333/collections/docmost-rag/points/search' \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "vector": [0.0, 0.0, 0.0], 
    "limit": 3,
    "with_payload": true,
    "filter": {"must": [{"key": "text", "match": {"text": "Hermannplatz "}}]}
  }'
