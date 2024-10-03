import json

def load_config():
    with open('config.json') as config_file:
        return json.load(config_file)

config = load_config()
API_KEY = config['API']['API_KEY']
IRIS_API_KEY = config['IRIS']['IRIS_API_KEY']
IRIS_HOST = config['IRIS']['IRIS_HOST']
VERIFY_CERTS = config['VERIFY_CERTS']
