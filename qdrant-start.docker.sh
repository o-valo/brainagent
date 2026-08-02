#!/bin/sh


docker run -d \
  --name qdrant \
  --restart always \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage:z \
  qdrant/qdrant
