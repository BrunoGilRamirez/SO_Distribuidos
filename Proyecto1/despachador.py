import time
from collections import deque
import random
import threading
import socket
import pickle
import Proceso

class Despachador:

    conn=None

    def __init__(self, quantum):

        self.cola_listos = deque()

        self.quantum = quantum

        self.lock = threading.Lock()

        self.serverAddress = "192.168.100.7"

        self.serverPort = 49152



    def agregar_proceso(self, proceso):

        with self.lock:

            self.cola_listos.append(proceso)

    def agregar_procesos(self, procesos):

        with self.lock:

            for proceso in procesos:

                self.cola_listos.append(proceso)



    def despachar_procesos(self):

        tiempo_total = 0

        while True:

            self.send_status()

            if len(self.cola_listos) == 0:

                print("No hay procesos en la cola de listos")

                time.sleep(random.randint(1, 3))

            else:

                with self.lock:

                    if not self.cola_listos:

                        break

                    proceso_actual = self.cola_listos.popleft()



                print("\n-------------------------------------------------------------")

                print(f"Despachando proceso: {proceso_actual.nombre}")

                tiempo_inicial = time.time()



                if proceso_actual.tiempo_ejecucion > self.quantum:

                    time.sleep(self.quantum)

                    proceso_actual.tiempo_ejecucion -= self.quantum

                    tiempo_total += self.quantum

                    with self.lock:

                        self.cola_listos.append(proceso_actual)

                else:

                    time.sleep(proceso_actual.tiempo_ejecucion)

                    tiempo_total += proceso_actual.tiempo_ejecucion

                    print(f"Proceso {proceso_actual.nombre} ejecutado durante {proceso_actual.tiempo_ejecucion} unidades de tiempo.")

                    print(f"Proceso {proceso_actual.nombre} finalizado.")



                tiempo_final = time.time()

                tiempo_ejecucion = tiempo_final - tiempo_inicial

                if tiempo_ejecucion < self.quantum:

                    time.sleep(self.quantum - tiempo_ejecucion)

                    tiempo_total += self.quantum - tiempo_ejecucion



        print(f"Tiempo total de ejecución: {tiempo_total}")

    def send_status(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

            server.connect((self.serverAddress, self.serverPort))

            status= {"name":"Despachador","charge":len(self.cola_listos)}

            server.sendall(pickle.dumps(status))

            print("Enviando estado")

            try:

                procesos=server.recv(1024)

                procesos=pickle.loads(procesos)

                print("Recibiendo procesos")

                for proceso in procesos:

                    print(f"Proceso recibido: {proceso.nombre} tiempo de llegada: {proceso.tiempo_llegada} tiempo de ejecucion: {proceso.tiempo_ejecucion}")

                    self.agregar_proceso(proceso)

            except:

                print("No hay procesos")

            server.close()

        

        

    





despachador = Despachador(2)

despachar = threading.Thread(target=despachador.despachar_procesos)

despachar.start()

