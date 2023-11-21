import time
import wmi


ProcesosProhibidos = []

contador = 0
i=0
c=wmi.WMI()

    
while(1):
    contador += 1
    if(contador == 10):
        f = open ('procesosProhibidos.txt','r')
        mensaje = f.read()
        print(mensaje)
        f.close()
        ProcesosProhibidos = mensaje.split('\n')
        print(ProcesosProhibidos)
        while(i<len(ProcesosProhibidos)):
            for process in c.Win32_process(Name=ProcesosProhibidos[i]):
                result, = process.Terminate()
                if result == 0:
                    print ("Process", process.Name, "stopped")
                else:
                    print ("Some problem")
                break
            else:
                print ("Process not found")
            i = i+1
        i=0
        contador=0
    time.sleep(1)
