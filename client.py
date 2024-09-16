import socket
import threading
import tkinter as tk
from tkinter import *
from tkinter import simpledialog  # Import for the name input dialog
from datetime import datetime


def get_user_name():
    user_name = simpledialog.askstring("Name", "Enter your name:")
    if user_name:
        return user_name
    else:
        return "User"

def send_message():
    message = message_entry.get()
    client.send(message.encode())
    message_entry.delete(0, tk.END)
    display_message(f"You: {message}")

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.startswith('/list'):
                # Display the list of connected clients
                client_list = message.split('\n')[1:]
                display_connected_clients(client_list)
            else:
                timestamp = datetime.now().strftime("%H:%M:%S")
                display_message(f"[{timestamp}] {message}")
        except:
            break

def display_message(message):
    message_display.insert(tk.END, message + "\n")
    message_display.see(tk.END)  # Scroll to the latest message

def display_connected_clients(client_list):
    client_display.delete(1.0, tk.END)  # Clear the existing list
    for client in client_list:
        client_display.insert(tk.END, client + "\n")

def main():
    global client, message_display, message_entry, client_display

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = 'localhost'  # Use 'localhost' when the server is running on the same machine
    server_port = 12345  # Use the same port as the server
    client.connect((server_ip, server_port))

    user_name = get_user_name()  # Get the user's name
    client.send( user_name.encode())

    root = tk.Tk()
    root.title("SIMPLE CHATTING APPLICATION")
    root.geometry("500x600")  # Set the initial size of the window

    # Create a custom color scheme
    background_color = "black"
    text_color = "white"
   

    root.configure(bg=background_color)

    title_label = Label(root, text=" ---- WELCOME ---- ", font=("Arial", 14, "bold"), fg="white", bg="red")
    title_label.pack(pady=10)

    title_label = Label(root, text="CHAT APPLICATION BY URWAH AND GROUP", font=("Arial", 14, "bold"), fg="white", bg="red")
    title_label.pack(pady=10)


    # Create labels, entry fields, and buttons for the UI
    message_display = tk.Text(root, bg=background_color, fg=text_color, font=("Helvetica", 12))
    message_display.pack()

    message_entry = tk.Entry(root, font=("Helvetica", 12))
    message_entry.pack()

    send_button = tk.Button(root, text="Send", command=send_message, bg="white", fg="black", font=("Helvetica", 16))
    send_button.pack()

    # Create a text widget to display the list of connected clients
    client_display = tk.Text(root, bg=background_color, fg=text_color, font=("Helvetica", 12))
    client_display.pack()

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()
print ("hello")
