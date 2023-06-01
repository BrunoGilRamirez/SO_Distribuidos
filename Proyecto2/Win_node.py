import socket
import threading
import os
import time
import pickle
import win_ctrl_c
import zipfile
import shutil
import hashlib
class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.files = []  # Lista de archivos compartidos por este nodo
        self.peers = []  # Lista de pares conocidos en la red
        self.pwd = './archivos/'
        self.folders = [] #Lista de carpetas compartidas por este nodo

    def start(self):
        # Iniciar el servidor en un hilo separado para aceptar conexiones entrantes
        server_thread = threading.Thread(target=self.start_server)
        self.known_peers = {"host1":('192.168.100.42', 5000),"localhost":('192.168.100.7', 5000)}
        server_thread.start()
        while True:
            self.check_files_in_folder()
            self.read_registry_file()
            print("\n","-" * 50, "Realizando conexion con los nodos conocidos", "-" * 50)
            for peer in self.known_peers:
                print(f"Archivos disponibles: {self.files}\n directorios disponibles: {self.folders}\n")
                print(f"Conectando a {self.known_peers[peer][0]}:{self.known_peers[peer][1]}")
                try:
                    self.connect_to_peer(self.known_peers[peer])
                except:
                    print(f"No se pudo conectar a {self.known_peers[peer][0]}:{self.known_peers[peer][1]}")
                print("|-"*100)
            print("-" * 50, "fin de conexion con nodos conocidos", "-" * 50, "\n")
            time.sleep(8)
            #detecta si en consola se hace ctrl+c para salir
            win_ctrl_c.install_handler()

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
        request = client_socket.recv(1024).decode(encoding='ascii', errors='replace')
        if request == 'list':
            # Enviar la lista de archivos al cliente
            file_list = pickle.dumps(self.files)
            client_socket.send(file_list)
            dir_list = pickle.dumps(self.folders)
            client_socket.send(dir_list)
        elif request.startswith('get'):
            # Extraer el nombre del archivo solicitado
            file_name = request.split()[1]
            if file_name in self.files:
                file_name = self.pwd + file_name
                # Enviar el archivo solicitado al cliente
                with open(file_name, 'rb') as file:
                    data = file.read(1024)
                    while data:
                        client_socket.send(data)
                        data = file.read(1024)
            else:
                client_socket.send("Archivo no encontrado".encode(encoding='ascii', errors='replace'))
        elif request.startswith('delete'):
            # Extraer el nombre del archivo solicitado
            file_name = request.split()[1]
            if file_name in self.files:
                file_name = self.pwd + file_name
                # Enviar el archivo solicitado al cliente
                try:
                    os.rmdir(file_name)
                    self.files.remove(file_name)
                    self.check_files_in_folder()
                except:
                    pass
                client_socket.send("Archivo eliminado".encode(encoding='ascii', errors='replace'))
            else:
                client_socket.send("Archivo no encontrado".encode(encoding='ascii', errors='replace'))
        elif request.startswith('receive_zip'):
            zip_name = request.split()[1]
            print(f"Recibiendo archivo {zip_name}")
            file = open(( self.pwd+zip_name), 'wb')
            data = client_socket.recv(1024)
            while data:
                file.write(data)
                data = client_socket.recv(1024)
            file.close()
            namedir = self.pwd+(zip_name.split(".")[0])
            shutil.rmtree(namedir, ignore_errors=True)
            print(f"archivo recibido {(self.pwd+zip_name)}, descomprimiendo en {namedir}")
            try:
                os.mkdir(namedir)
            except:
                pass
            try:
                shutil.unpack_archive((self.pwd+zip_name), namedir)
            except:
                print("No se pudo descomprimir el archivo")
            os.remove((self.pwd+zip_name))
            self.check_files_in_folder()
            print("archivo descomprimido")
            #client_socket.send("Archivo recibido".encode(encoding='ascii', errors='replace'))
        client_socket.close()

    def check_files_in_folder(self):
        file_list = os.listdir(self.pwd)
        self.files = [file for file in file_list if os.path.isfile((self.pwd + file))]
        self.folders = [folder for folder in file_list if os.path.isdir((self.pwd + folder))]

    def connect_to_peer(self, ipport):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            peer_socket.connect(ipport)
            # Enviar solicitud para obtener la lista de archivos
            peer_socket.send("list".encode(encoding='ascii', errors='replace'))
            file_list = peer_socket.recv(1024)
            file_list = pickle.loads(file_list)
            dir_list = peer_socket.recv(1024)
            dir_list = pickle.loads(dir_list)
            print(f"Archivos disponibles en {ipport[0]}:{ipport[1]}:\n{file_list}")
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
            try: 
                for folder in self.folders:
                    if (folder not in dir_list)or (self.folders_have_changed(folder)):
                        self.compress_andSenddirectory(ipport, folder)
                self.check_files_in_folder()
            except:
                print("No se pudo descargar el archivo")
        except ConnectionRefusedError:
            print(f"No se pudo conectar a {ipport[0]}:{ipport[1]}")

    def folders_have_changed(self,folder_name):
        # Crear un hash vacío
        current_hash = hashlib.md5()
        for root, dirs, files in os.walk((self.pwd + folder_name)):
            for file in files:
                file_path = os.path.join(root, file)
                # Actualizar el hash con el contenido y metadatos del archivo
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    #current_hash.update(file_data) # Actualizar el hash con el contenido del archivo
                    current_hash.update(file.encode(encoding='ascii', errors='replace')) # Actualizar el hash con el nombre del archiv
        # Comprobar si el hash ha cambiado desde la última vez
        previous_hash = self.load_previous_hash(folder_name)
        if previous_hash != current_hash.hexdigest():
            self.save_current_hash(folder_name,current_hash.hexdigest())
            print(f"El directorio {folder_name} ha cambiado")
            return True
        return False

    def load_previous_hash(self,folder_name):
        # Cargar el hash almacenado previamente (si existe)
        if os.path.exists(f'./hashes/{folder_name}_hash.txt'):
            with open(f'./hashes/{folder_name}_hash.txt', 'r') as f:
                return f.read()
        return None

    def save_current_hash(self,folder_name,hash_value):
        # Guardar el hash actual
        with open(f'./hashes/{folder_name}_hash.txt', 'w') as f:
            f.write(hash_value)

    def compress_andSenddirectory(self, ipport, folder):
        zip_file = folder + ".zip"
        zip_name = self.pwd + folder
        try:
            zippath= shutil.make_archive(zip_name, 'zip', zip_name)
            zippath = zippath.replace('\\', '/')
        except:
            print("No se pudo comprimir el archivo")
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            peer_socket.connect(ipport)
            peer_socket.send(f"receive_zip {zip_file}".encode(encoding='ascii', errors='replace'))
            with open(zippath, 'rb') as file:
                print(f"Enviando {zip_file} a {ipport[0]}:{ipport[1]}")
                data = file.read(1024)
                while data:
                    peer_socket.send(data)
                    data = file.read(1024)
            peer_socket.close()
        except ConnectionRefusedError:
            print(f"No se pudo conectar a {ipport[0]}:{ipport[1]}")


    def download_file(self, ipport, file_name):
        peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        peer_socket.connect(ipport)
        # Enviar solicitud para obtener el archivo
        peer_socket.send(f"get {file_name}".encode(encoding='ascii', errors='replace'))
        # Crear el archivo 
        file_name = self.pwd + file_name
        file = open(file_name, 'wb')
        data = peer_socket.recv(1024)
        while data:
            file.write(data)
            data = peer_socket.recv(1024)
        file.close()
        peer_socket.close()
    
            
    def read_registry_file(self):
        #Esta funcion lee el archivo delete.txt y elimina los archivos que se encuentren en el de todos los nodos
        with open("delete.txt", "r") as file:
            files_to_delete = file.read()
            files_to_delete = files_to_delete.split("\n")
            print(files_to_delete)
            for file in self.files:
                if file in files_to_delete:
                    self.delete_file(file)

    def delete_file(self, file_name):
        #this function deletes the file from all nodes
        print("deleting file")
        for peer in self.known_peers:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                peer_socket.connect(self.known_peers[peer])
                # Enviar solicitud para obtener el archivo
                peer_socket.send(f"delete {file_name}".encode(encoding='ascii', errors='replace'))
                print(peer_socket.recv(1024))
                peer_socket.close()
            except:
                print(f"No se pudo conectar a {self.known_peers[peer][0]}:{self.known_peers[peer][1]}")
        try:
            file_name = self.pwd + file_name
            os.remove(file_name)
        except:
            pass
        self.check_files_in_folder()



# Ejemplo de uso
if __name__ == '__main__':
    # Crear y configurar los nodos de la red
    peer1 = Peer('0.0.0.0', 5000)
    # Iniciar los nodos en hilos separados
    treadServer = threading.Thread(target=peer1.start).start()

