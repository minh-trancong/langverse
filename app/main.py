import requests
import json

# Define the base URL
base_url = "https://www.anphatpc.com.vn/ajax/get_json.php?action=collection&action_type=list&id="

# Loop over the IDs
for id in range(890, 975):
    # Send a GET request to the API
    response = requests.get(base_url + str(id))

    # Parse the response as JSON
    data = response.json()

    # Save the JSON data to a file
    with open(f'data/data_{id}.json', 'w') as f:
        json.dump(data, f)