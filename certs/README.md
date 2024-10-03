## Generating Certificates

You can either generate self-signed SSL certificates automatically or provide your own. They should replace the private.key and public.crt files in the certs directory. 

### Option 1: Auto-Generate Certificates

Run the provided script to generate SSL certificates:

```bash
./generate_certs.sh
```

### Option 2: Overwrite Existing Certificates

If you prefer to use your own certificates, place them in the `certs` directory. If you name them something else you will need to modify the Dockerfile in the ngninx.directory:

- `private.key` (your SSL private key)
- `public.crt` (your SSL certificate)
