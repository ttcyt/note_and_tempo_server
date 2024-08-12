import requests

url = 'http://127.0.0.1:5000/process_audio'
audio_file_path = '化成路29巷 6.wav'

with open(audio_file_path, 'rb') as f:
    audio_data = f.read()

response = requests.post(url, data=audio_data)

if response.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)