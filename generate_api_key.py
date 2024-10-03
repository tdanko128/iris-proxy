import secrets

def generate_secure_api_key(length=64):
    # Generate a secure random key and convert it to a hex string
    return secrets.token_hex(length)

# Generate the API key
api_key = generate_secure_api_key(128)
print(api_key)
