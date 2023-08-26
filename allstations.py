import json
import requests

url = "https://wbgtgroup9.azurewebsites.net/all_current"

def predict_wbgt():
    result_dict = {}
    try:
        response = requests.get(url=url)
        data = response.json()
        data = json.loads(data)
    except Exception as e:
        print(e)

    for record in data:
        station_id = record["station_id"]
        wbgt = record["WBGT"]
        result_dict[station_id] = wbgt
    return result_dict

predict_wbgt()