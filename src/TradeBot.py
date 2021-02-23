import requests
import json


with open("secrets.json") as f:
  data = json.load(f)


print(data)
