


def get_proxy_dict(port):
    return {
            "http": "http://" + port,
            "https": "https://" + port,
            "ftp": "ftp://10.10.1.10:3128"
        }