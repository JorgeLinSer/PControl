import wmi
from pysnmp.hlapi import *
from pysnmp.entity.rfc3413.oneliner import cmdgen

import socket #for sockets
import sys #for exit



contador=0
i = 0

#create an INET (i.e. IPv4), STREAMing (i.e. TCP) socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print ('Failed to create socket')
    sys.exit()
    
print ('Socket Created')
host = '127.0.0.1'
port = 5000

#Connect to remote server
s.connect((host , port))
print ('Socket Connected to ' + host)

        
def SolicitarProcesos():
    lista=[]
    
    errorIndication, errorStatus, errorIndex, \
    varBindTable = cmdgen.CommandGenerator().bulkCmd(  
                cmdgen.CommunityData('Public', mpModel=0),  
                cmdgen.UdpTransportTarget(('127.0.0.1', 161)),  
                0, 
                25, 
                (1,3,6,1,2,1,25,4,2,1,2), # OID tabla procesos
            )

    if errorIndication:
       print (errorIndication)
    else:
        if errorStatus:
            print ('%s at %s\n' % (
                errorStatus.prettyPrint(),
                errorIndex and varBindTable[-1][int(errorIndex)-1] or '?'
                ))
        else:
            for varBindTableRow in varBindTable:
                for name, val in varBindTableRow:
                    lista.append(val.prettyPrint())

    return lista

def MataProceso(nombreProceso):
    
    c=wmi.WMI()

    for process in c.Win32_process(Name=nombreProceso):
      result, = process.Terminate()
      if result == 0:
        print ("Process", process.Name, "stopped")
      else:
        print ("Some problem")
      break
    else:
      print ("Process not found")
      
    return


while(1):
    data = s.recv(4096)
    print(data.decode())
    opcion=int(data.decode())
    data = s.recv(4096)
    print(data.decode())
    cadena=data.decode()
    if(opcion == 1):
        procesos = SolicitarProcesos()
        procesos = ", ".join(procesos)
        s.sendall(procesos.encode())
        
    if(opcion == 2):
        MataProceso(cadena)
        
    if(opcion == 3):
        f = open ('procesosProhibidos.txt','a')
        f.write('\n' + cadena)
        f.close()

    if(opcion == 4):
        s.close()
