# Flask App with Nginx Proxy for DFIR IRIS Alerts

This repository contains a Flask application that processes Microsoft Sentinel incident payloads and transforms the data into alerts for DFIR IRIS. The app is deployed using Docker with an Nginx proxy for secure access.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Generating Certificates](#generating-certificates)
- [Customize Nginx](#customize-nginx)
- [Docker Setup](#docker-setup)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone the repository:

   ```bash
   git clone https://github.com/tdanko128/iris-proxy.git
   cd iris-proxy
   ```

2. Make sure you have the necessary permissions to run scripts:

   ```bash
   chmod +x generate_certs.sh
   ./generate_certs.sh
   ```

3. Generate an API Key for the app:
   ```bash
   python3 generate_api_key.py
   ```

4. Copy the configuration template:

   ```bash
   cp config.json.template config.json
   ```

5. Open `config.json` and fill in the required fields according to your environment.  If you use the script you will need to copy the result into the config.json file.  
   ```json
   {
      "API": {
         "API_KEY": "your_api_key_here"
      },
      "IRIS": {
         "IRIS_API_KEY": "your_iris_api_key",
         "IRIS_HOST" : "your_fqdn_for_iris"
      },
      "VERIFY_CERTS" : true
   }
   ```
   - You can create your own api key or use the script to create one for `API.API_KEY`.
   - You should get an API key for an account that has permissions to add alerts in IRIS and set it for `IRIS.IRIS_API_KEY`
   - If you are running on the same host as the DFIR-Iris instance you should use `172.17.0.1` or `host.docker.internal`.
   - Set `VERIFY_CERTS` to `true` if your certs are signed by a Trusted CA, otherwise set it to `false`.

6. Build and start the Docker containers:

   ```bash
   docker compose build
   docker compose up 
   ```

7. Test API to Flask App and Iris
   FLASK:
   ```bash
   curl -X GET https://localhost:8443/api/test/flask -H "Authorization: Bearer YOUR_API_KEY" --insecure
   ```
   IRIS:
   ```bash
   curl -X GET https://localhost:8443/api/test/iris -H "Authorization: Bearer YOUR_API_KEY" --insecure
   ```

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

## Customize Nginx

If you would like to customize the configuration of nginx you can edit `nginx.conf` file in the `nginx` directory. Make sure any changes are also refelected in the `Dockerfile(s)` and or `docker-compose.yml`. 

## Docker Setup

1. Build and start the Docker containers:

   ```bash
   docker compose build
   docker compose up -d
   ```

2. Check the status of your containers:

   ```bash
   docker ps
   ```

The Flask app should now be accessible through the Nginx proxy on port `8443`.


## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
```

Feel free to modify the content as necessary, especially the sections for usage and any additional details specific to your application!