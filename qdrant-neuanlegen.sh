#!/bin/sh



curl -X PUT http://192.168.2.42:6333/collections/docmost-rag \
  -H 'Content-Type: application/json' \
  --data-raw '{
    "vectors": {
      "size": 768,
      "distance": "Cosine"
    }
  }'
