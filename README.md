# Security Policy Conflict Detection  in SDN

This project dynamically detects the con-compliant security flow rules based on user Intents.

## Contributor
Neha Vadnere

## System Requirements
- OS: Ubuntu 18.04
- SDN Controller: ONOS
- Data-plane emulation: Mininet
- Supporting Software Packages: Python2.7, python-3.6, git, zip, curl, unzip, bazel-3.0.0, mavel-3.3.9, karaf-3.0.5, java-11

## Installation

Install required software packages first. Start ONOS controller and run a sample mininet topology.

To run ONOS controller server in localhost -

bazel run onos-local -- clean build

 
To start given mininet topology, run this command in separate terminal.

    sudo ./run.sh

Start ONOS cli in a new terminal.

    cd $ONOS_ROOT (where you have installed ONOS)
    ./tools/test/bin/onos onos@localhost
    (Default password: rocks)

Start required packages to start openflow services and basic l2 forwarding services in ONOS cli window.

    onos > app activate org.onosproject.openflow
    onos > app activate org.onosproject.fwd

Add any required intent request in onos cli. (Example given below)

    onos > add-host-intent 00:00:00:00:00:01/None 00:00:00:00:00:02/None 

This will add a new Intent from host h1 to h2. (00:00:00:00:00:01/None  si host h1's id and 00:00:00:00:00:02/None is host h2's id.

Add some flowrule to drop the packets based on specific criteria. One example is given below.

    python3 DefaultDropApp_poc.py

Run some functions to start off the applications.

    python3 main.py

You can see the results of the reports generated in ***"Results"*** folder.
***report.txt*** will display consolidated report of number of conflicts detected and details of that conflict.

## Video Link for Demo
[Project Demo](https://asu.zoom.us/rec/share/6xZ-xLi6e5iLlmHPasBIboelO-8b54bBtEONqlwZ9F4Bi30Vp70webrh7iBoW4CX.P9hj8JjrW0QZwLQr) (Passcode: .ur2F@C&)






