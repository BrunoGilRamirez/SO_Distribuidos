import socket
import threading
import os
import time
import pickle

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.files = []  # Lista de archivos compartidos por este nodo
        self.peers = []  # Lista de pares conocidos en la red

    def start(self):
        # Iniciar el servidor en un hilo separado para aceptar conexiones entrantes
        server_thread = threading.Thread(target=self.start_server)
        self.known_peers = {"host1":('192.168.100.42', 5000),"localhost":('192.168.100.7', 5000)}
        server_thread.start()
        while True:
            self.check_files_in_folder()
            self.read_registry_file()
            for peer in self.known_peers:
                print("\n"* 10,"-" * 50)
                print(f"Archivos disponibles: {self.files}")
                print(f"Conectando a {self.known_peers[peer][0]}:{self.known_peers[peer][1]}")
                try:
                    self.connect_to_peer(self.known_peers[peer])
                except:
                    print(f"No se pudo conectar a {self.known_peers[peer][0]}:{self.known_peers[peer][1]}")
                print("-" * 50, "\n")
            time.sleep(8)

    def start_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Servidor iniciado en {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            # Iniciar un hilo para manejar la conexión entrante
            threading.Thread(target=self.handle_connection, args=(client_socket,)).start()

    def handle_connection(self, client_socket):
        request = client_socket.recv(1024).decode()
        if request == 'list':
            # Enviar la lista de archivos al cliente
            file_list = pickle.dumps(self.files)
            client_socket.send(file_list)
        elif request.startswith('get'):
            # Extraer el nombre del archivo solicitado
            file_name = request.split()[1]
            if file_name in self.files:
                # Enviar el archivo solicitado al cliente
                with open(file_name, 'rb') as file:
                    data = file.read(1024)
                    while data:
                        client_socket.send(data)
                        data = file.read(1024)
            else:
                client_socket.send("Archivo no encontrado".encode())
        elif request.startswith('delete'):
            # Extraer el nombre del archivo solicitado
            file_name = request.split()[1]
            if file_name in self.files:
                # Enviar el archivo solicitado al cliente
                os.remove(file_name)
                self.files.remove(file_name)
                client_socket.send("Archivo eliminado".encode())
            else:
                client_socket.send("Archivo no encontrado".encode())

        client_socket.close()

    def check_files_in_folder(self):
        
        file_list = os.listdir('.')
        self.files = [file for file in file_list if os.path.isfile(file)]


    def connect_to_peer(self, ipport):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            peer_socket.connect(ipport)
            # Enviar solicitud para obtener la lista de archivos
            peer_socket.send("list".encode())
            file_list = peer_socket.recv(1024)
            file_list = pickle.loads(file_list)
            print(f"Archivos disponibles en {ipport[0]}:{ipport[1]}: Tipo: {type(file_list)} \nArchivos: {file_list}")
            self.peers.append(ipport)
            peer_socket.close()
            if (set(self.files)!=set(file_list)):
                try: 
                    for file in file_list:
                        if file not in self.files:
                            self.download_file(ipport, file)
                    self.check_files_in_folder()
                except:
                    print("No se pudo descargar el archivo")
            else:
                print("No hay archivos nuevos")
        except ConnectionRefusedError:
            print(f"No se pudo conectar a {ipport[0]}:{ipport[1]}")

    def download_file(self, ipport, file_name):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect(ipport)
        # Enviar solicitud para obtener el archivo
        peer_socket.send(f"get {file_name}".encode())
        file = open(file_name, 'wb')
        data = peer_socket.recv(1024)
        while data:
            file.write(data)
            data = peer_socket.recv(1024)
        file.close()
        peer_socket.close()
    
    def overwrite_file(self):
        with open("notdelete.txt", "w") as file:
            content = '\n'.join(self.files)
            file.write(content)
            file.close()

            
    def read_registry_file(self):
        #this function creates if file doesn´t, and reads the name of the files must be deleted from all nodes
        print("reading file")
        with open("delete.txt", "r") as file:
            files_to_delete = file.read()
            files_to_delete = files_to_delete.split("\n")
            print(files_to_delete)
            for file in self.files:
                if file in files_to_delete:
                    self.delete_file(file)

    def delete_file(self, file_name):
        #this function sends notdelete.txt to all nodes 
        # and delete the file from the local node
        os.remove(file_name)
        self.files.remove(file_name)
        self.check_files_in_folder()
        for peer in self.known_peers:
            print(peer)
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                peer_socket.connect(self.known_peers[peer])
                with open("delete.txt", "rb") as file:
                    data = file.read(1024)
                    while data:
                        peer_socket.send(data)
                        data = file.read(1024)
                peer_socket.close()
            except ConnectionRefusedError:
                print(f"No se pudo conectar a {self.known_peers[peer][0]}:{self.known_peers[peer][1]}")



# Ejemplo de uso
if __name__ == '__main__':
    # Crear y configurar los nodos de la red
    peer1 = Peer('0.0.0.0', 5000)
    # Iniciar los nodos en hilos separados
    threading.Thread(target=peer1.start).start()