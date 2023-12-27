import socket
import threading

# Define a class to represent a client
class ClientNode:
    def __init__(self, name, socket, address):
        self.name = name
        self.socket = socket
        self.address = address

# Initialize the list to store connected clients and a lock for thread safety
connected_clients = []
lock = threading.Lock()

def add_client(client_node):
    """Add a client to the list of connected clients."""
    with lock:
        connected_clients.append(client_node)

def remove_client(client_node):
    """Remove a client from the list of connected clients."""
    with lock:
        connected_clients.remove(client_node)

def broadcast(message, sender):
    """Broadcast a message to all connected clients except the sender."""
    with lock:
        for client in connected_clients:
            if client != sender:
                try:
                    client.socket.send(message.encode())
                except:
                    # Handle the case where the client socket is no longer available
                    remove_client(client)
                    print(f"Removed {client.name} from the list")
                    
# Add the process_command function here
def process_command(command, client_node):
    """Process client commands and send appropriate responses."""
    if command.startswith('/list'):
        client_names = [client.name for client in connected_clients]
        response = '\n'.join(client_names)
        client_node.socket.send(response.encode())

def handle_client(client_socket, address):
    """Handle communication with a client."""
    client_name = client_socket.recv(1024).decode()
    print(f"{client_name} connected from {address[0]}:{address[1]}")
    client_node = ClientNode(client_name, client_socket, address)
    add_client(client_node)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            if message.startswith('/'):
                # Process commands
                process_command(message, client_node)
            else:
                # Regular chat message
                print(f"Received from {client_name}: {message}")
                broadcast(f"{client_name}: {message}", client_node)
        except:
            # Handle exceptions when receiving messages or processing commands
            break

    remove_client(client_node)
    print(f"{client_name} disconnected from {address[0]}:{address[1]}")
    client_socket.close()


# Create a server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '0.0.0.0'
port = 12345
server.bind((host, port))
server.listen(5)
print(f"Server listening on {host}:{port}")

while True:
    client_sock, addr = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_sock, addr))
    client_handler.start()
