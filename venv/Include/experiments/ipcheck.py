import requests
from filedata import *
from utils.tools import get_proxy_dict


def testipCheck():
    # data = nameList[1]
    # print(data)
    for data in nameList:
        try:
            port = data.split("*")[1]
            mla_profile_id = data.split("*")[0]
            # proxyDict = {
            #
            # }
            proxyDict = get_proxy_dict(port)
            firstipcheck = requests.get('https://api.ipify.org/', proxies=proxyDict)
            print(firstipcheck.content)
        except:
            pass


if __name__ == "__main__":
    testipCheck()