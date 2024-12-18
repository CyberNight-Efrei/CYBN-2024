#!/usr/bin/env python3
import os
import socket as s

# Configuration
LISTEN_PORT = 1001

FORWARD_HOST = '10.44.10.143'
FORWARD_PORT = 9991

FLAG = os.environ.get('FLAG', 'Woops. Une erreur est survenue, mais vous avez effectivement eu le flag. Contactez un admin.')

"""
Heyyy ! Encore du code pourri (réfère toi à BGM si tu veux encore plus de rant) ! Quel génie l'auteur de ce code, hein ?!
J'espère que t'as aimé la CyberNight (surtout avec le bypass frauduleux inhérent à ce challenge) parce qu'après ça
je suis inembauchable...
"""

def forward_message(sock, message):
    try:
        sock.sendall(message)

        response = b""
        while True:
            chunk = sock.recv()
            if not chunk:
                break
            response += chunk

        # response = sock.recv(1024)
        # Wait for response

        # Forward response back to client
        return sock, response
    except Exception:
        sock.close()
        try:
            sock = s.socket(s.AF_INET, s.SOCK_STREAM)
            sock.connect((FORWARD_HOST, FORWARD_PORT))
            sock.settimeout(None)

            # Try again just once
            sock.sendall(message)
            response = sock.recv(1024)

            return sock, response
        except Exception:
            pass
    return b"dead", b"dead"


def main():
    try:
        java_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        java_socket.connect((FORWARD_HOST, FORWARD_PORT))
        java_socket.settimeout(None)
    except ConnectionRefusedError as e:
        exit(e.errno)

    java_socket, ping = forward_message(
        java_socket,
        ("check_queue\n" + os.environ.get('CONTAINER_CREATOR') + "\n").encode()
    )
    ping = ping.strip(b" \r\n")
    if ping == b"dead":
        print(b"Une erreur est survenue...")
        return
    elif ping == b"in_queue":
        print("Oi ! Tu crois que t'es seul ici ?! Attends ton tour !")
        return
    print("""Bon, je vais pas tourner autour du pot.
Entre ton mot a 48 bits et je te dirai si lumiere sera... ou pas.
Format : e0e1e2...e45e46e47
Exemple : 101010101010101010101010101010101010101010101010

Bonne chance :)


""")
    answer = input(">>> ").strip()
    if len(answer) != 48:
        print("Pfff, serieusement ? J'ai dit 48 bits ! Allez, j'me tire.")
        return
    elif any(c not in "01" for c in answer):
        print("T'as pas compris ce que je t'ai dit ??? C'est des 0 et des 1 et rien d'autre !")
        return

    print("En voila une belle reponse ! Je reviens vers toi, un instant...\n\n")

    java_socket, java_res = forward_message(
        java_socket,
        ("solution\n" + os.environ.get('CONTAINER_CREATOR') + "\n" + answer + "\n").encode()
    )

    java_res = java_res.strip(b" \r\n").decode()
    if java_res == "dead":
        print("Une erreur est survenue...")
    elif java_res == "will_do":
        response = java_socket.recv(1024).decode().strip(" \r\n")

        if response == "win":
            print("Wow, j'y crois pas !\n")
            print("Voici ton flag : " + FLAG)
        elif response == "lose":
            print("Dommage, ce n'est pas le bon mot...")
        elif response == "in_queue":
            print("Hé ! T'as cru que j'allais te donner la réponse comme ça ?! Attends un peu !")
    else:
        print("Une erreur est survenue...")


if __name__ == "__main__":
    main()
