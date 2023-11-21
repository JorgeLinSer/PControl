import socket
import sys

import time

class Admin:

    def __init__(self,nombre,puerto,log):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.PORT = puerto
        self.nombre = nombre
        self.HOST = ''
        self.log = log

        try:
            self.s.bind((self.HOST, self.PORT))
        except socket.error as e:
            self.log ('Bind failed. Error Code : ' + str(e.errno) + ', Message: ' +
            e.strerror )
            return
            
        self.s.listen(10)

        #wait for connection and return a new socket and the remote address
        self.conn, self.addr = self.s.accept()
        self.log (self.nombre + ' conectado con ' + self.addr[0] + ':' + str(self.addr[1]))
        return

    def listarProcesos(self):
        opcion = 1
        mensaje=" "
        self.conn.sendall(str(opcion).encode())
        time.sleep(1)
        self.conn.sendall(mensaje.encode())
        data = self.conn.recv(4096)
        cadena = data.decode()
        lista = cadena.split(", ")
        lista = set(lista)
        return lista

    def matarProceso(self, proceso):
        opcion = 2
        self.conn.sendall(str(opcion).encode())
        time.sleep(1)
        self.conn.sendall(proceso.encode())
        return
    
    def prohibirProceso(self,proceso):
        opcion = 3
        self.conn.sendall(str(opcion).encode())
        time.sleep(1)
        self.conn.sendall(proceso.encode())
        return

    def desconectar(self):
        opcion = 4
        mensaje = " "
        self.conn.sendall(str(opcion).encode())
        time.sleep(1)
        self.conn.sendall(mensaje.encode())
        self.s.close()
        return
                
                
            
                            
            
        
