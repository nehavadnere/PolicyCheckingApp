import requests
import json
from logger import *
import os

class ControllerCommunicator:
    def __init__(self):
        self.logger = get_logger(str(os.path.basename(__file__)))

    def connect(Self):
        URL = "http://localhost:8181/onos/v1/flows?appIdd=org.onosproject.cli"
        header = {"Content-type": "application/json", "Accept":"application/json"}
        URL = "http://localhost:8181/onos/v1/flows/"

        r = requests.get(URL, auth=('onos','rocks'))
        print(r.text)
        file1 = open("Flows.json","w+")
        file1.write(r.text)
        file1.close()

    def main(Self):
        print("here")
        #ControllerCommunicator.connect();

if __name__ == "__main__":
    c = ControllerCommunicator();
    c.connect()

