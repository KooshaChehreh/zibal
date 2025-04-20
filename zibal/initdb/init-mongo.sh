#!/bin/bash
echo "Starting MongoDB initialization..."

# Decompress the .agz file
gzip -d /docker-entrypoint-initdb.d/transaction.agz

# Import the decompressed BSON file into MongoDB
mongorestore --gzip --archive=/docker-entrypoint-initdb.d/transaction.bson --db zibaldb

echo "MongoDB initialization complete."