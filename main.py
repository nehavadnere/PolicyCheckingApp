import os
from GetFlows import ControllerCommunicator
import json
import requests
from logger import *

class IntentParser:
    def __init__(self):
        self.logger = get_logger(str(os.path.basename(__file__)))
        self.flowrules = {}

    def writeFile(self, content, filename, outputPath):
        #file1 = open(filename,"w+")
        #file1.write(content)
        #file1.close()
        with open(outputPath + os.path.sep + filename, "w", encoding='utf-8') as write_file:
            write_file.write(json.dumps(content,ensure_ascii=True))

    '''
    This api parse the ONOS configuration and creates a dictionary of flow rules
    '''
    def parseOnosConfiguration(self, config):

        self.onosFlowJson = config
        opf ={}
        rules = []

        for flow in self.onosFlowJson:
            flowType = flow["treatment"]["instructions"][0]["type"]
            flowPort = flow["treatment"]["instructions"][0]["port"]
            if flowType == "OUTPUT" and flowPort != "CONTROLLER":
                rule = {}
                lines = []
                rule["deviceId"] = flow["deviceId"]
                rule["id"] = flow["id"]

                #Parse selector criteria one by one
                criteria = flow["selector"]["criteria"]
                for items in criteria:
                    lines.append(items)
                rule["criteria"] = lines
                
                #Parse selector criteria one by one
                lines_inst = []
                instructions = flow["treatment"]["instructions"]
                for items in instructions:
                    lines_inst.append(items)
                self.logger.info("lines :: " +str(lines_inst))
                rule["instruction"] = lines_inst

                rules.append(rule)
        opf["rules"] = rules
        self.flowrules = opf
        self.logger.info("rules ::" +str(self.flowrules))
        self.writeFile(self.flowrules, "ParsedFlows.json", "Results")

    def main(self):
        #c = ControllerCommunicator();
        #c.connect();
        f =open("Flows.json","r")
        data = json.loads(f.read())

        self.parseOnosConfiguration(data["flows"])

        self.logger.info("Identification of segments from ONOS configuration Success")

        outDir = "Results" + os.path.sep + "sdn"

        #self.writeFile(self.flowrules, "ParsedFlows.json",outDir)


if __name__ == "__main__":
    parser = IntentParser();
    parser.main();
