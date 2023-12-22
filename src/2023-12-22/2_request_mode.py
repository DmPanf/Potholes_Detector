# 2_request_mode.py
import requests
import json


my_string = '''
{
  "modes": [
    "Basic",
    "Grid",
    "HQ-SAM",
    "YOLOv8"
  ],
  "active_mode": "YOLOv8"
}
'''

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
    data = response.json()
    print("Response Content:", data)
    print("---------------------------------------")

    # If 'Modes_List' is a key in the response, print its value directly
    if 'Modes_List' in data:
        print("Modes List:", data['Modes_List'])
    print("---------------------------------------")

# Testing endpoints
#test_endpoint("modes/Basic", method='post')  # POST mode
test_endpoint("modes")


#my_list = json.loads(my_string)['modes']
#print(f'\n{my_list}')
