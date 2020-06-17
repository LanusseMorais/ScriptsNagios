#!/usr/bin/python3
from pysnmp import hlapi
from sys import argv,exit

def getStatus(host, vpn, community=hlapi.CommunityData('public'), port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData(),):
    
    identityNamePhaseTwo=hlapi.ObjectIdentity('SNMPv2-SMI','enterprises','12356.101.12.2.2.1.3')
    identityStatusPhaseOne=hlapi.ObjectIdentity('SNMPv2-SMI','enterprises','12356.101.12.2.2.1.20')

    namePhaseOne = hlapi.bulkCmd(
        engine,
        community,
        hlapi.UdpTransportTarget((host, port)),
        context, 0,2,hlapi.ObjectType(identityNamePhaseTwo))
    
    statusPhaseOne = hlapi.bulkCmd(
        engine,
        community,
        hlapi.UdpTransportTarget((host, port)),
        context, 0,2,hlapi.ObjectType( identityStatusPhaseOne))

    bindName = next(namePhaseOne)
    bindStatus = next(statusPhaseOne)
    vpnList = {}
    while (identityNamePhaseTwo.prettyPrint() in  str(bindName[3][-1])):
        key = str(bindName[3][-1]).split(' = ')[1].lower()
        item = str(bindStatus[3][-1]).split(' = ')[1]
        vpnList[key]=item
        bindName = next(namePhaseOne)
        bindStatus = next(statusPhaseOne)
  
    return vpnList[vpn]


if __name__ == "__main__":
    if len(argv) < 3:
        print(""" !!Parâmentros incorretos!!

        ./check_vpn_snmp.py host vpn
        """)
    else:
        host =argv[1]
        vpn = argv[2].lower()
        if getStatus(host,vpn) == "1":
            print("DOWN")
            exit(2)
        else:
            print("UP")
            exit(0)
        
        
        