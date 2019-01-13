import requests
import json


def test():
    print(r"46.101.125.90:8080/schedule/3/0000")
    url = r"http://46.101.125.90:8080/schedule/3/0000"
    resp = requests.get(url, auth=('admin', 'password'))
    print(resp.status_code)
    # print(resp.content)
    json_data = json.loads(resp.content.decode("utf-8"))
    print(len(json_data))
    for data in json_data:
        for subdata in data:
            print(subdata.keys())

if __name__ == "__main__":
    test()