#!/bin/sh

curl -X POST 'http://192.168.2.42:6333/collections/docmost-rag/points/delete' \
  -H 'Content-Type: application/json' \
  --data-raw '{"filter": {"must": [{"has_id": [0, 1000000000]}]}}'
