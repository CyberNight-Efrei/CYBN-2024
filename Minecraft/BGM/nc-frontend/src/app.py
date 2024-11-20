import os
import socket as s

# Configuration
LISTEN_PORT = 1001

FORWARD_HOST = '10.44.10.143'
FORWARD_PORT = 9991

FLAG = os.environ.get('FLAG', 'Woops. Une erreur est survenue, mais vous avez effectivement eu le flag. Contactez un admin.').encode()


def forward_message(sock, message):
    try:
        print("Forwarding message:", message)
        sock.sendall(message)

        response = b""
        while True:
            chunk = sock.recv()
            if not chunk:
                break
            response += chunk

        # response = sock.recv(1024)
        # Wait for response
        print("Response:", response)

        # Forward response back to client
        return sock, response
    except Exception:
        print("Trying to reconnect to Java server...")
        sock.close()
        try:
            sock = s.socket(s.AF_INET, s.SOCK_STREAM)
            sock.connect((FORWARD_HOST, FORWARD_PORT))
            sock.settimeout(None)

            # Try again just once
            sock.sendall(message)
            response = sock.recv(1024)
            print("Response:", response)

            return sock, response
        except Exception:
            # pas de message d'erreur pour les participants... :(
            print("Could not connect to Java server:")
            print("Is the Java server running ?")
            exit(-1)
    return b"dead", b"dead"


def main():
    try:
        java_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        java_socket.connect((FORWARD_HOST, FORWARD_PORT))
        java_socket.settimeout(None)
    except ConnectionRefusedError as e:
        print("Could not connect to Java server:", e)
        print("Is the Java server running ?")
        exit(e.errno)

    with (s.socket(s.AF_INET, s.SOCK_STREAM) as this_server):
        this_server.bind(("127.0.0.1", LISTEN_PORT))
        this_server.listen(1)
        print("Listening on port", LISTEN_PORT)
        client, client_info = this_server.accept()
        print(client_info)

        java_socket, ping = forward_message(
            java_socket,
            ("check_queue\n" + os.environ.get('CONTAINER_CREATOR') + "\n").encode()
        )
        ping = ping.strip(b" \r\n")
        if ping == b"dead":
            client.sendall(b"Une erreur est survenue...")
            return
        elif ping == b"in_queue":
            client.sendall(b"Oi ! Tu crois que t'es seul ici ?! Attends ton tour !" + b"\n")
            return
        client.sendall(b"""Bon, je vais pas tourner autour du pot.
Entre ton mot a 48 bits et je te dirai si lumiere sera... ou pas.
Format : e0e1e2...e45e46e47
Exemple : 101010101010101010101010101010101010101010101010

Bonne chance :)


>>> """)
        answer = client.recv(64).decode().strip()
        if len(answer) != 48:
            client.sendall("Pfff, serieusement ? J'ai dit 48 bits ! Allez, j'me tire.".encode())
            return
        elif any(c not in "01" for c in answer):
            client.sendall("T'as pas compris ce que je t'ai dit ??? C'est des 0 et des 1 et rien d'autre !".encode())
            return

        client.sendall("En voila une belle reponse ! Je reviens vers toi, un instant...\n\n".encode())
        print("Answer:", answer)

        java_socket, java_res = forward_message(
            java_socket,
            ("solution\n" + os.environ.get('CONTAINER_CREATOR') + "\n" + answer + "\n").encode()
        )
        print(java_res)
        java_res = java_res.strip(b" \r\n").decode()
        if java_res == "dead":
            client.sendall("Une erreur est survenue...".encode())
        elif java_res == "will_do":
            response = java_socket.recv(1024).decode().strip(" \r\n")
            print(response)
            if response == "win":
                client.sendall("Wow, j'y crois pas !\n".encode())
                client.sendall("Voici ton flag : ".encode() + FLAG)
            elif response == "lose":
                client.sendall("Dommage, ce n'est pas le bon mot...".encode())
            elif response == "in_queue":
                client.sendall("Hé ! T'as cru que j'allais te donner la réponse comme ça ?! Attends un peu !".encode())
        else:
            client.sendall("Une erreur est survenue...".encode())


if __name__ == "__main__":
    main()
