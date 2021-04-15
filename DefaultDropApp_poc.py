'''
    APP DESCRPIPTION: THIS APPLICATION IS A PROOF OF CONCEPT FOR DEMONSTATING 
    HOW CAN WE ESTABLISH A DEFAULT DROP POLICY IN SDN BASED SWITCH.

    IN ONOS SDN, FLOW RULES ARE INSTALLED IN THE SWITHCES USING INTENTS
    OR OTHER APPLICATIONS. HOWEVER, IN CASE OF PACKETS FOR WITH MATCHING RULE
    IS NOT FOUND IN THE FLOW RULES IN THE SWITCHES, THAT PACKET IS SENT TO THE
    SDN CONTROLLER TO TAKE THE DECISION ON ADD/DROP OR ANY OTHER ACTION TO BE
    TAKEN ON THAT PACKET.

    IN OUR SCHENARIO, WE DO NOT WISH TO OVERBURDEN THE SDN CONTROLLER BY SENDING
    MESSAGES LIKE THIS. HENCE THIS APPLICATION INSTALLS A DEFAULT LOW-PRIORITY
    FLOW RULE WHICH WILL DROP THE PACKETS. SINCE IT IS THE LOWEST PRIORITY RULE,
    ALL OTHER RULES ARE CHECKED AT FIRST BEFORE THIS RULE HITS.
'''
import requests
import json
import codecs

#Content type must be included in the header
header = {"content-type": "application/json", "Accept": "application/json"}
url = "http://localhost:8181/onos/v1/flows?appId=org.onosproject.cli"
#flow1 = {
flow1 = {"flows" : [
  {
  "priority": 4123,
  "timeout":0,
  "isPermanent": "true",
  "deviceId":"of:0000000000000001",
  "treatment": {
    "instructions": [
      {
        "type": "OUTPUT",
        "port": 2
      }
    ]
  },
  "selector": {
    "criteria": [
      {
        "type": "ETH_TYPE",
        "ethType": "0x88cc"
      },
	  {
        "type": "ETH_SRC",
        "mac": "00:00:00:00:00:01"
      }
    ]
  }
}
]
}
default_flow = {"flows" : [
  {
  "priority": 100,
  "timeout":0,
  "isPermanent": "true",
  "deviceId":"of:0000000000000001",
  "treatment": {
  },
  "selector": {
    "criteria": [
      {
        "type": "ETH_TYPE",
        "ethType": "0x800"
      },
      {
        "type": "IPV4_SRC",
        "ip": "10.0.0.1/24"
      }
    ]
  }
}
]
}


with codecs.open("DropFlow.json", "r", encoding="utf-8") as f:
    dropFlow = json.load(f)


#send default flowrule to switch
flow_url = "http://localhost:8181/onos/v1/flows/"
r = requests.post(url, data=json.dumps(dropFlow), headers=header, auth=('onos', 'rocks'))
print(r.status_code, r.reason)
print (r.text)

#get all flow details
r = requests.get(flow_url, auth=('onos','rocks'))
print(r.status_code, r.reason)
print (r.text)


f.close()
