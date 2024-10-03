import requests
from custom_modules.config import IRIS_API_KEY, IRIS_HOST, VERIFY_CERTS

def send_iris_alert(body):
    url = f"https://{IRIS_HOST}/alerts/add"  # Replace with your API endpoint
    headers = {
        "Content-Type": "application/json",  # Change if needed
        "Authorization": f"Bearer {IRIS_API_KEY}"  # Optional: Add if your API requires authentication
    }
    
    try:
        response = requests.post(url, json=body, headers=headers, verify=VERIFY_CERTS)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        return {"success": True, "data": response.json()}  # Return success response
    except requests.exceptions.HTTPError as http_err:
        return {
            "success": False,
            "error": f"HTTP error occurred: {http_err}",
            "status_code": http_err.response.status_code  # Include the HTTP status code
        }
    except Exception as err:
        return {"success": False, "error": f"An error occurred: {err}"}

def test_iris():
    url = f"https://{IRIS_HOST}/api/ping"  # Replace with your API endpoint
    headers = {
        "Content-Type": "application/json",  # Change if needed
        "Authorization": f"Bearer {IRIS_API_KEY}"  # Optional: Add if your API requires authentication
    }
    
    try:
        response = requests.get(url, headers=headers, verify=VERIFY_CERTS)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        return {"success": True, "data": response.json()}  # Return success response
    except requests.exceptions.HTTPError as http_err:
        return {
            "success": False,
            "error": f"HTTP error occurred: {http_err}",
            "status_code": http_err.response.status_code  # Include the HTTP status code
        }
    except Exception as err:
        return {"success": False, "error": f"An error occurred: {err}"}