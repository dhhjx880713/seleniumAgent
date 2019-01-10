import json
import requests
import time
from random import randint
import random
def main():

    ports = []
    for x in range(1):
        ports.append(4376+x)
        print(4376+x)

    for x in range(20):
        for y in ports:
            createprofile(y)
            time.sleep(10)


def createprofile(portnumber):
    languages = ["de-DE,de;q=0.9", "de-DE", "de-DE,en;q=0.9", "de", "de,de-DE;q=0.9,en;q=0.8", "de-DE,de;q=0.9",
                 "de-DE,de;q=0.9", "de-DE,de;q=0.9", "de-DE,de;q=0.9", "de-DE"]
    browsertypes = ["stealth_fox", "mimic"]
    dontrack = ["0", "0", "0", "0", "0", "0", "0", "0", "1", "1", "1"]
    permittype = ["request", "request", "request", "request", "request", "block", "block", "always"]
    canvas = ["NOISE", "NOISE", "NOISE", "NOISE", "block", "block"]
    url = 'https://api.multiloginapp.com/v1/profile/create?token=aba4a97e76bc6905f1e83e9d10781ce1662bb522'
    renderers = [
        "ANGLE (AMD Radeon R7 250 Series Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD Radeon(TM) R6 Graphics Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics 520 Direct3D9Ex vs_3_0 ps_3_0)",
        "ANGLE (Intel(R) HD Graphics 520 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD Radeon(TM) HD 6520G Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD Radeon HD 7540D Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD 760G Direct3D11 vs_4_0 ps_4_0)",
        "ANGLE (Intel(R) Iris(TM) Graphics 540 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics 5300 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (ATI Radeon 3000 Graphics Direct3D11 vs_4_0 ps_4_0)",
        "ANGLE (AMD Radeon HD 5450 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (ATI Radeon 3000 Graphics Direct3D11 vs_4_0 ps_4_0)",
        "ANGLE (ATI Mobility Radeon HD 4200 Series Direct3D11 vs_4_1 ps_4_1)",
        "ANGLE (AMD Radeon HD 5570 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD Radeon HD 7450 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (ATI Radeon 3000 Graphics Direct3D11 vs_4_0 ps_4_0)",
        "ANGLE (ATI Radeon HD 5450 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0)",
        "ANGLE (Intel(R) HD Graphics 4000 Direct3D9Ex vs_3_0 ps_3_0)",
        "ANGLE (Intel(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics Direct3D11 vs_4_1 ps_4_1)",
        "ANGLE (NVIDIA GeForce 8500 GT Direct3D11 vs_4_0 ps_4_0)",
        "ANGLE (AMD Radeon (TM) R9 370 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics Family Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA GeForce GT 730 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics 4600 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics 520 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA GeForce GTX 1070 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (ATI Radeon HD 5470 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0)",
        "ANGLE (NVIDIA GeForce GTX 970 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD Radeon(TM) R4 Graphics Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD Radeon HD 8450G Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics 520 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD Radeon HD 8210 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics 530 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics 3000 Direct3D11 vs_4_1 ps_4_1)",
        "ANGLE (NVIDIA GeForce 7025 / NVIDIA nForce 630a Direct3D9Ex vs_3_0 ps_3_0)",
        "ANGLE (Intel(R) HD Graphics Family Direct3D9Ex vs_3_0 ps_3_0)",
        "ANGLE (Intel(R) HD Graphics 610 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (NVIDIA GeForce GTS 450 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD Radeon(TM) R2 Graphics Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (AMD Radeon R7 200 Series Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics Family Direct3D11 vs_5_0 ps_5_0)",
        "ANGLE (Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0)"
    ]
    payload = {
      "name": portnumber,
      "browserType": random.choice(browsertypes),
      "proxyHost": "195.154.161.119",
      "proxyPort": portnumber,
      "proxyType": "HTTP",
      "tag": portnumber,
      "disablePlugins": True,
      "disableFlashPlugin": True,
      "canvasDefType": random.choice(canvas),
      "maskFonts": True,
      "doNotTrack": random.choice(dontrack),
      "langHdr": random.choice(languages),
      "timeZoneFillOnStart": True,
      "forbidConcurrentExecution": True,
      "audio": {
        "noise": True
      },
      "geolocation": {
        "permitType": random.choice(permittype),
        "fillOnStart": True,
        "accuracy": 10
      },
      "webgl": {
        "noise": True,
        "vendor": "Google Inc.",
        "renderer": random.choice(renderers),
      },
      "mediaDevices": {
        "audioInputs": randint(0, 4),
        "audioOutputs": randint(0, 4),
        "videoInputs": randint(0, 1)
      },
      "webRtc": {
        "type": "FAKE",
        "fillOnStart": True,
        "localIps": [
          "192.168.1."+str(randint(2, 15))
        ]
      },
      "generateZeroFingerprintsData": True
    }
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.status_code)
    print(json.dumps(payload, indent=4, sort_keys=True))



if __name__ == "__main__":
    main()