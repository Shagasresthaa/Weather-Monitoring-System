import requests

url = "http://127.0.0.1:5000/"

data = requests.get(url + "helloworld")

print(data.json())