from seleniumAgent import SeneliumAgent
from filedata import *
import argparse


def main():
    parser = argparse.ArgumentParser(description="Start the selenium agent rest inferface")
    parser.add_argument("-rest_server_address", default=r'http://46.101.125.90:8080/schedule/')
    parser.add_argument("-port", default="195.154.161.119:4399")
    args = parser.parse_args()
    timeout = 15
    resend_time = 15
    agent = SeneliumAgent(port=args.port,
                          rest_server_address=args.rest_server_address, timeout=timeout, debug=True)
    agent.run()


if __name__ == "__main__":
    main()