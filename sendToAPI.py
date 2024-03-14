import requests

api_endpoint = "/upload_csv"
api_url = f"https://linktreeapianalytics.pythonanywhere.com{api_endpoint}"

csv_file = 'test_data_table.csv'

files = {'file': ('test.csv', open(csv_file, 'rb'), 'text/csv')}

response = requests.post(api_url, files=files)

print(response.text)

