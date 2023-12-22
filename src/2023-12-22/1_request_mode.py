# 1_request_mode.py
import requests

# Base URL of your FastAPI server
BASE_URL = "http://localhost:8001"

def test_endpoint(endpoint, method='get', data=None):
    url = f"{BASE_URL}/{endpoint}"
    if method == 'get':
        response = requests.get(url)
    elif method == 'post':
        response = requests.post(url, json=data)
    else:
        raise ValueError("Method not supported")
    
    print('\n---------------------------------------')
    print(f"Testing {method.upper()} {url}")
    print("Response Status:", response.status_code)
    print("Response Content:", response.json())
    print("---------------------------------------")

# Testing endpoints
test_endpoint("")  # Root endpoint
test_endpoint("info")  # Info endpoint
test_endpoint("modes")  # GET modes
test_endpoint("modes/YOLOv8", method='post')  # POST mode (replace 'test_mode' with a valid mode)
test_endpoint("models")  # Models endpoint
