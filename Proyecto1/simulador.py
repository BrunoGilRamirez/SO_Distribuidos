from Proceso import Proceso
import time
import threading
import socket
import pickle
import random
from despachador import Despachador
class Simulador:
    def __init__(self, cantidad_procesos, quantum, ipserver = "192.168.100.7", port = 49152):
        self.cantidad_procesos = cantidad_procesos
        self.quantum = quantum
        self.server = socket.create_server((ipserver, port))

    def generar_procesos(self):
        procesos = []
        for i in range(1, self.cantidad_procesos + 1):
            nombre = f"P{i}"
            tiempo_llegada = random.randint(0, self.cantidad_procesos - 1)
            tiempo_ejecucion = random.randint(1, 10)
            proceso = Proceso(nombre, tiempo_llegada, tiempo_ejecucion)
            procesos.append(proceso)
        return procesos

    def simular(self):
            despachador = Despachador(self.quantum)
            
            procesos = self.generar_procesos()

            for proceso in procesos:
                despachador.agregar_proceso(proceso)
            print("Primera ronda de procesos agregados a la cola de listos.")
            thread = threading.Thread(target=despachador.despachar_procesos)
            thread.start()
            # Agregar más procesos mientras se ejecuta el despacho
            proceso3 = Proceso("proceso 3", 3, 3)
            proceso4 = Proceso("Proceso 4", 2,2)
            time.sleep(2)
            despachador.agregar_proceso(proceso4)
            despachador.agregar_proceso(proceso3)
            print("----------------------------------------------------------")
            print("|Segunda ronda de procesos agregados a la cola de listos.|")
            print("----------------------------------------------------------")

            # Esperar a que el hilo de despacho termine
            #thread.join()
    def send_Proceso(self,conn):
        with conn:
            list_procesos = self.generar_procesos()
            for proceso in list_procesos:
                print(proceso.nombre)
            conn.sendall(pickle.dumps(list_procesos))

            
    def receiveStatusFromOthers(self):
        with  self.server as server:
            print(f"servidor desde {server}")
            while True:
                conn, addr = server.accept()
                with conn:
                    print("Conexión establecida con", addr)
                    data = conn.recv(1024)
                    status = pickle.loads(data)
                    print("Status del proceso:", status)
                    if status["charge"]==0:
                        self.send_Proceso(conn)
                        print("Procesos enviado")
                    conn.close()
                    print("Conexion cerrada")




simulador = Simulador(cantidad_procesos=5, quantum=2, ipserver="172.18.107.124")
simulador.receiveStatusFromOthers()