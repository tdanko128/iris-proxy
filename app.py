from flask import Flask, request, jsonify
import json
from custom_modules.convert_incident import convert_to_iris_alert
from custom_modules.config import API_KEY  # Import the API key from the config module
from custom_modules.send_to_iris import send_iris_alert, test_iris

app = Flask(__name__)

def validate_api_key(auth_header):
    if auth_header is None:
        return False
    try:
        # Extract the token from the 'Bearer' prefix
        prefix, api_key = auth_header.split()
        return prefix.lower() == "bearer" and api_key == API_KEY
    except ValueError:
        return False

@app.post('/api/incident/add')
def add_incident():
    # Get the Authorization header
    auth_header = request.headers.get('Authorization')
    if not validate_api_key(auth_header):
        return jsonify({"error": "Unauthorized","message":"If you don't belong here stay the fuck out"}), 401
    
    # Process the incident
    data = request.get_json()
    alert = convert_to_iris_alert(data)

    # Forward to IRIS
    result = send_iris_alert(alert)
    if result['success']:
        return jsonify(result.get('data',{})), 201
    else:
        if result.get('status_code', None):
            status_code = result['status_code']
        else:
            status_code = 500
        return jsonify(result), status_code

@app.get('/api/test/flask')
def test_api_flask():
    # Get the Authorization header
    auth_header = request.headers.get('Authorization')
    if not validate_api_key(auth_header):
        return jsonify({"error": "Unauthorized","message":"If you don't belong here stay the fuck out"}), 401
    return jsonify({"Response": 200, "Status": "Success"}), 200

@app.get('/api/test/iris')
def test_api_iris():
    # Get the Authorization header
    auth_header = request.headers.get('Authorization')
    if not validate_api_key(auth_header):
        return jsonify({"error": "Unauthorized","message":"If you don't belong here stay the fuck out"}), 401
        # Forward to IRIS
    result = test_iris()
    if result['success']:
        return jsonify(result.get('data',{})), 200
    else:
        if result.get('status_code', None):
            status_code = result['status_code']
        else:
            status_code = 500
        return jsonify(result), status_code




if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)