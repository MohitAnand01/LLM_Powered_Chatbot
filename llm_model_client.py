import requests
def send_call_to_llm(data):
    # URL to send the POST request to
    url = "https://16ab-35-231-87-161.ngrok-free.app/"
    # Data to send with the request (can be a dictionary, JSON, etc.)
    data = data
    print(data)
# Making the POST request
    response = requests.post(url, data=data)

# Checking if the request was successful
    if response.status_code == 200:
        print("Request was successful.")
        print("Response Text:", response.text)
    else:
        print("Request failed. Status code:", response.status_code)
