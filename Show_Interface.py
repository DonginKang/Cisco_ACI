# -*- coding: utf8 -*-

#!/usr/bin/env python
#
# Written by Mike Timm @ cisco System, March 2014
# Revised by Toru Okatsu @ Cisco Systems, June 11th 2014


# list of packages that should be imported for this code to work
import re
import cobra.mit.access
import cobra.mit.session

APIC = "IP"
USER = "USER"
PASS = "PASSWORD"

# get an interface name and an index 
# the index is slot_id * 200 + port_id
# assume one slot has no more than 200 ports
def getIfName(intf):
    # phy interface name is like phys-[eth1/98]
    name = None
    idx = None

    match = re.search('\[(eth\d+/\d+)\]', str(intf.dn))
    if match:
        name = match.group(1)
        match = re.search('(\d+)/(\d+)', name)
        if match:
            idx = 200*int(match.group(1)) + int(match.group(2))

    return name, idx 

########
# Main #
########

# log into an APIC and create a directory object

url = "https://" + APIC
ls = cobra.mit.session.LoginSession(url, USER, PASS, secure=False, timeout=180) 
md = cobra.mit.access.MoDirectory(ls)
md.login()

# Get the list of pods
while(1):
    pods = md.lookupByClass("fabricPod", parentDn='topology')
    for mo in pods:
        print "\n\n\nname = {}".format(mo.rn)
      
    for pod in pods:

    # Get nodes under one pod
        dn = pod.dn
        nodes = md.lookupByClass("fabricNode", parentDn=dn)
        for node in nodes:
            print "Node: {:10s} Name: {:10s} Role: {:10s}".format(node.rn, node.name, node.role)

    
        select = raw_input("\n\nInput node name or 'all' : ")
        status = raw_input("Input status : ")
    

        for node in nodes:
            # Skip APICs and unsupported switches
            if node.role == 'controller' or node.fabricSt != 'active':
                continue

    
            if node.name == select:

                print "\nNode Name: " + node.name
        # l1PhysIf has the name of interface and admin status
        # ethpmPhysIf has the operation status
                dn = str(node.dn) + '/sys'
                intfs = md.lookupByClass("l1PhysIf", parentDn=dn) 
                pmifs = md.lookupByClass("ethpmPhysIf", parentDn=dn)

                iftable = {}
                for intf in intfs:
                    name, idx = getIfName(intf)
                    if name and idx:
                        iftable[idx] = [name, intf.adminSt, "Unknown"]
                for intf in pmifs:
                    name, idx = getIfName(intf)
                    if name and idx:
                        list = iftable[idx]
                        list[2] = intf.operSt
                        iftable[idx] = list

            # print the interface status
                for idx, list in sorted(iftable.items()):
                    if list[2] == status:
                        print list[0], list[1], list[2]
                    if status == 'all':
                        print list[0], list[1], list[2]
                break

            if select == "all":

                print "\nNode Name: " + node.name
        # l1PhysIf has the name of interface and admin status
        # ethpmPhysIf has the operation status
                dn = str(node.dn) + '/sys'
                intfs = md.lookupByClass("l1PhysIf", parentDn=dn) 
                pmifs = md.lookupByClass("ethpmPhysIf", parentDn=dn)

                iftable = {}
                for intf in intfs:
                    name, idx = getIfName(intf)
                    if name and idx:
                        iftable[idx] = [name, intf.adminSt, "Unknown"]
                for intf in pmifs:
                    name, idx = getIfName(intf)
                    if name and idx:
                        list = iftable[idx]
                        list[2] = intf.operSt
                        iftable[idx] = list

        # print the interface status
                for idx, list in sorted(iftable.items()):
                    if list[2] == status:
                        print list[0], list[1], list[2]  
                    if status == 'all':
                        print list[0], list[1], list[2]



