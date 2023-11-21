from tkinter import *
from tkinter import ttk
from tkinter import Text, END, messagebox

from clase_admin import Admin

class Gestor:

    def __init__(self, window):
        self.listOfPCs = []
        self.procesosProhibidos = []
        self.logLinea = 1

        self.window = window
        self.window.geometry("600x300")
        self.window.resizable(False, False)
        self.window.title("Gestor")

        
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
       
        ttk.Button(self.window, text="Listar Pc's gestionados", command=self.manage_pc_popup).grid(column=0, row=0, sticky=W+E+S+N)
        ttk.Button(self.window, text="Añadir Pc", command=self.add_pc_popup).grid(column=0, row=1, sticky=W+E+S+N)
        ttk.Button(self.window, text="Añadir proceso prohibido", command=self.add_prohibited_process_popup).grid(column=0, row=2, sticky=W+E+S+N)

        self.outputText = Text(self.window, state="disabled")
        self.outputText.grid(column=1, row=0, rowspan=3, sticky=W+E+S+N)


    def add_pc_popup(self):
        addPc = Toplevel(self.window)
        addPc.title("Añadir Pc")

        ttk.Label(addPc, text="Introduzca un nombre: ").grid(row=0, column=0)
        nameInput = ttk.Entry(addPc)
        nameInput.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

        ttk.Label(addPc, text="Introduzca un puerto: ").grid(row=1, column=0)
        portInput = ttk.Entry(addPc)
        portInput.grid(row=1, column=1, padx=(5, 5), pady=(5, 5))

        ttk.Label(addPc, text="Tras hacer click en Añadir, el programa se bloquea hasta que se establece la conexión!").grid(row=2, column=0, columnspan=2, padx=(5, 5), pady=(5, 5))
        ttk.Button(addPc, text='Añadir', command= lambda: self.add_pc(addPc, nameInput.get(), portInput.get())).grid(row=3, column=0, columnspan=2, padx=(5, 5), pady=(5, 5))
        addPc.resizable(False, False)

    def add_pc(self, popup, name, port):
        self.listOfPCs.append(Admin(name, int(port), self.log))
        popup.destroy()


    def manage_pc_popup(self):
        if len(self.listOfPCs) == 0:
            messagebox.showinfo("Gestionar Pcs", "No hay Pc's registrados.")
        else:
            managePc = Toplevel(self.window)
            managePc.title("Manage Pcs")
            for idx in range(len(self.listOfPCs)):
                displayName = "[Nombre] " + self.listOfPCs[idx].nombre + " | [IP] " + self.listOfPCs[idx].addr[0]
                ttk.Label(managePc, text=displayName).grid(row=idx, column=0, padx=(5, 5), pady=(5, 5))
                ttk.Button(managePc, text='Eliminar', command= lambda: self.remove_pc(managePc, self.listOfPCs[idx])).grid(row=idx, column=1, padx=(5, 5), pady=(5, 5))
                ttk.Button(managePc, text='Ver Procesos', command= lambda: self.list_processes(managePc, self.listOfPCs[idx])).grid(row=idx, column=2, padx=(5, 5), pady=(5, 5))
                ttk.Button(managePc, text='Matar Un Proceso', command= lambda: self.choose_process_to_kill(self.listOfPCs[idx])).grid(row=idx, column=3, padx=(5, 5), pady=(5, 5))
            managePc.resizable(False, False)


    def remove_pc(self, popup, pc):
        pcName = pc.nombre
        self.listOfPCs.remove(pc)
        self.log(pcName + " eliminado.")
        popup.destroy()


    def list_processes(self, popup, pc):
        runningProcesses = pc.listarProcesos()
        self.log("Procesos en ejecución para " + pc.nombre + ":")
        for process in runningProcesses:
            self.log("- " + process)
        popup.destroy()


    def choose_process_to_kill(self, pc):
        chooseProcess = Toplevel(self.window)
        chooseProcess.title("Matar un proceso")

        ttk.Label(chooseProcess, text="Introduzca el nombre del proceso a matar: ").grid(row=0, column=0, padx=(5, 5), pady=(5, 5))
        nameInput = ttk.Entry(chooseProcess)
        nameInput.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

        ttk.Button(chooseProcess, text='Matar', command= lambda: self.kill_process(chooseProcess, pc, nameInput.get())).grid(row=1, column=0, columnspan=2, padx=(5, 5), pady=(5, 5))
        chooseProcess.resizable(False, False)


    def kill_process(self, popup, pc, proceso):
        pc.matarProceso(proceso)
        self.log("Se ha matado el proceso: " + proceso + " en: " + pc.nombre)
        popup.destroy()


    def add_prohibited_process_popup(self):
        addProhibited = Toplevel(self.window)
        addProhibited.title("Añadir proceso prohibido")

        ttk.Label(addProhibited, text="Introduzca el nombre del proceso a prohibir: ").grid(row=0, column=0, padx=(5, 5), pady=(5, 5))
        nameInput = ttk.Entry(addProhibited)
        nameInput.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))

        ttk.Button(addProhibited, text='Añadir', command= lambda: self.add_prohibited_process(addProhibited, nameInput.get())).grid(row=1, column=0, columnspan=2, padx=(5, 5), pady=(5, 5))
        addProhibited.resizable(False, False)


    def add_prohibited_process(self, popup, proceso):
        self.procesosProhibidos.append(proceso)
        self.log("Lista actual de los procesos prohibidos:")
        for procesoProhibido in self.procesosProhibidos:
            self.log("- " + procesoProhibido)

        for pc in self.listOfPCs:
            self.log("Mandando el nombre del proceso prohibido a: " + pc.nombre)
            pc.prohibirProceso(proceso)

        popup.destroy()


    def log(self, logMessage):
        self.outputText.configure(state="normal")
        self.outputText.insert(END, str(self.logLinea) + ". " + logMessage + "\n")
        self.outputText.configure(state="disabled")
        self.logLinea = self.logLinea + 1


root = Tk()
Gestor(root)
root.mainloop()