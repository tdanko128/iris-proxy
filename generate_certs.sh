#!/bin/bash

# Create the certs directory if it doesn't exist
mkdir -p ./certs

# Generate a self-signed certificate
openssl req -x509 -newkey rsa:2048 \
  -keyout ./certs/private.key \
  -out ./certs/public.crt \
  -days 365 -nodes \
  -subj "/CN=localhost"

echo "Self-signed certificate and key have been generated in ./certs."
