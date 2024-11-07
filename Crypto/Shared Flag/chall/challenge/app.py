import os
import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.number import getPrime, long_to_bytes
from Crypto.Util.Padding import pad

FLAG = os.environ.get('FLAG', 'Une erreur est survenue, contactez les admins sur discord.')


def show_intro(g, p, A):
    print(f"""
                     _____ _                        _   ______ _             
                    / ____| |                      | | |  ____| |            
                   | (___ | |__   __ _ _ __ ___  __| | | |__  | | __ _  __ _ 
                    \___ \| '_ \ / _` | '__/ _ \/ _` | |  __| | |/ _` |/ _` |
                    ____) | | | | (_| | | |  __/ (_| | | |    | | (_| | (_| |
                   |_____/|_| |_|\__,_|_|  \___|\__,_| |_|    |_|\__,_|\__, |
                                                                        __/ |
                                                                       |___/ 
    
Bienvenue !

J'ai réussi à voler un flag à ces stupides organisateurs de la CyberNight, j'imagine que ça t'intéresse ?
Comme j'ai un peu pitié de toi, je veux bien te le partager mais j'ai peur qu'on nous écoute...
On a qu'à utiliser Diffie-Hellman tiens ! Envoie moi ta clé publique et je t'enverrai la mienne avec le flag chiffré

Voici les paramètres que j'ai choisi :
    - g : {g}
    - p : {p}
    - A : {A}
""")

def encrypt_flag(secret: int) -> str:
    key = hashlib.md5(long_to_bytes(secret)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(FLAG.encode(), AES.block_size)).hex()


def main():
    g = 1337
    p = getPrime(512)
    private_a = random.randrange(2, p - 1)
    public_a = pow(g, private_a, p)

    show_intro(g, p, public_a)

    try:
        public_b = int(input("> "))
    except:
        print(f"\nJ'ai pas le temps de niaiser ! Si tu veux pas me donner ta clé, débrouille toi")
        exit()

    if not 1 < public_b < (p-1):
        print("\nJ'ai des connaissances en maths que tu n'as pas, essaie de me duper et je détruis le flag")
        exit()
    
    secret_shared = pow(public_b, private_a, p)
    print(f"""
T'as vraiment cru que j'allais te passer un flag gratuitement ?
Amuses toi bien à le déchiffrer sans ma clé publique :)

Ton flag : {encrypt_flag(secret_shared)}""")
    exit()


if __name__ == '__main__':
    main()
