import os
from GetFlows import ControllerCommunicator
import json
import requests
from logger import *
from netaddr import EUI, mac_unix_expanded
import time

class IntentParser:
    def __init__(self):
        self.logger = get_logger(str(os.path.basename(__file__)))
        self.flowrules = {}
        self.exactMatch = {}
        self.beginT = 0
        self.endT = 0
        self.report = ""
        self.conflictCount = 0

    def writeFileJson(self, content, filename, outputPath):
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
            print(flow)
            flowType = flow["treatment"]["instructions"][0]["type"]
            if flowType == "OUTPUT":
                flowPort = flow["treatment"]["instructions"][0]["port"]
            if flowType == "OUTPUT" or flowType =="NOACTION":
                if flowType == "NOACTION" or (flowType == "OUTPUT" and flowPort != "CONTROLLER"):
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
                    rule["instruction"] = lines_inst

                    rules.append(rule)
        opf["rules"] = rules
        self.flowrules = opf

        #TODO remove immendiate next 2 lines - this is only for testing
        #f =open("test.json","r")
        #self.flowrules = json.loads(f.read())

        self.logger.info("rules ::" +str(self.flowrules))
        self.writeFileJson(self.flowrules, "ParsedFlows.json", "Results")

    def getAction(self,i,rule):
        return rule["instruction"]

    def getCriteria(self,i,rule):
        return rule["criteria"]

    def getValue(self,rule,param):
        c = rule["criteria"]
        for i,val in enumerate(c):
            if c[i]["type"] == param:
                if param == "ETH_SRC" or param == "ETH_DST":
                    fn_mac = EUI(c[i]["mac"], dialect=mac_unix_expanded)
                    return fn_mac
                if param == "IP_SRC" or param == "IP_DST":
                    return c[i]["ip"]
                if param == "IN_PORT":
                    return c[i]["port"]
            i+=1
    
    def writeFile(self, content, filename, outputPath):
        filefull = outputPath + os.path.sep + filename
        file1 = open(filefull,"a+")
        file1.write(content)
        file1.close()

    def evalTime(self):
        executionTime = (self.endT - self.beginT) * 1000 #in microseconds
        num_flows = len(self.onosFlowJson)
        content = str(num_flows)+ "," + str(executionTime) +"\n"
        self.writeFile(content,"eval.csv", "Results")

    def generateReport(self):
        rep = "\n--------------------------------------------------------------\n"
        rep += "                  CONFLICT CHECKING REPORT                    \n"
        rep += "--------------------------------------------------------------\n\n"
        rep += self.report
        self.writeFile(rep , "report.txt", "Results")

    def flowPolicyCheck(self, n_index,fn, e_index, fe):
        criteria = []
        actions = []

        #get the criteria for new flowrule and existing flowrule
        criteria_fn = self.getCriteria(n_index,fn)
        criteria_fe = self.getCriteria(e_index,fe)
        
        #get the action for new flowrule and existing flowrule
        action_fn = self.getAction(n_index,fn)
        action_fe = self.getAction(e_index,fe)

        #check only for same device
        self.logger.info("device 1 = " + fn["deviceId"]+ " device 2 = "+ fe["deviceId"])
        if fn["deviceId"] == fe["deviceId"]:
            sameDevice = True
        else:
            sameDevice = False

        #proceed checking only of both rules are in same switch
        if not sameDevice:
            return

        ethSrcMatch = ethDstMatch = inPortMatch = exactMatch = duplicate = conflict = 0

        #check selection criteria for new flowrule and existing flowrule
        if criteria_fn == criteria_fe:
            exactSame = True
            id_fn = fn["id"]
            id_fe = fe["id"]
            rules = []
            rules.append(criteria_fn)
            rules.append(criteria_fe)
            self.logger.info("Exact Matching ( " +id_fn+ ", " +id_fe+ " ) ")

        id_fn = fn["id"]
        id_fe = fe["id"]

        self.logger.info("src 1 = " + str(self.getValue(fn,"ETH_SRC"))+ " src 2 = "+ str(self.getValue(fe,"ETH_SRC")))
        self.logger.info("dst 1 = " + str(self.getValue(fn,"ETH_DST"))+ " dst 2 = "+ str(self.getValue(fe,"ETH_DST")))
        self.logger.info("inpoer 1 = " + str(self.getValue(fn,"IN_PORT"))+ " inport 2 = "+ str(self.getValue(fe,"IN_PORT")))


        if self.getValue(fn,"ETH_SRC") == self.getValue(fe,"ETH_SRC"):
                ethSrcMatch = 1
        if self.getValue(fn,"ETH_DST") == self.getValue(fe,"ETH_DST"):
                ethDstMatch = 1
        if self.getValue(fn,"IN_PORT") == self.getValue(fe,"IN_PORT"):
                inPortMatch = 1

        if ethSrcMatch and ethDstMatch and inPortMatch:
            exactMatch = True
            self.logger.info("Exact Matching ( " +id_fn+ ", " +id_fe+ " ) \n   ::  "+str(self.getCriteria(0,fn)))

        if action_fn[0]["type"] == action_fe[0]["type"] == "OUTPUT":
            checkPort = True
        else:
            checkPort = False
        if checkPort and action_fn[0]["port"] == action_fe[0]["port"] and exactMatch:
            duplicate = True
            self.logger.info("Duplicate Rule ( " +id_fn+ ", " +id_fe+ " ) ")
            self.conflictCount += 1
            self.report += "\n\n CONFLICT #" +str(self.conflictCount)+ ": \n -----------"
            self.report += "\nDuplicate Rule ( " +id_fn+ ", " +id_fe+ " ) "
            self.report += "\n\t Criteria :: " + str(self.getCriteria(0,fn))
            self.report += "\n\t Action   :: " + str(self.getAction(0,fn))
        
        if action_fn[0]["type"] == "NOACTION" or action_fe[0]["type"] == "NOACTION" and exactMatch:
            duplicate = True
            self.logger.info("Conflict Rule ( " +id_fn+ ", " +id_fe+ " ) ")
            self.conflictCount += 1
            self.report += "\n\n CONFLICT #" +str(self.conflictCount)+ ": \n -----------"
            self.report += "\nConflict Rule ( " +id_fn+ ", " +id_fe+ " ) "
            self.report += "\n\t Criteria :: " + str(self.getCriteria(0,fn))
            self.report += "\n\t Actions  :: " + str(self.getAction(0,fn)) + "\t" + str(self.getAction(0,fe))
        
        ethSrcMatch = ethDstMatch = inPortMatch = exactMatch = duplicate = conflict = 0
        

    def flowPolicyCheckAll(self):
        numFlows =  len(self.flowrules)
        for i,newFlow in enumerate(self.flowrules["rules"]):
            for j,existingFlow in enumerate(self.flowrules["rules"]):
                if j>i:
                    self.beginT = time.time()
                    self.flowPolicyCheck(i,newFlow, j,existingFlow)
                    self.endT = time.time()
                j+=1
            i+=1

    def main(self):
        c = ControllerCommunicator();
        c.connect();
        f =open("Flows.json","r")
        data = json.loads(f.read())

        self.parseOnosConfiguration(data["flows"])

        self.flowPolicyCheckAll()

        self.evalTime()

        self.generateReport()



if __name__ == "__main__":
    parser = IntentParser();
    parser.main();
