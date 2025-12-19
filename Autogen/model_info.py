import requests

url = "https://openrouter.ai/v1/models/nvidia/nemotron-3-nano-30b-a3b:free"
headers = {
    "Authorization": "Bearer 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"
}

resp = requests.get(url, headers=headers)
print("Status code:", resp.status_code)
print("Response text:", resp.text)

