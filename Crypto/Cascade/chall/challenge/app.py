import os
from Crypto.Cipher import AES


BANNER = """
 _____                 _                 _
|  __ \               (_)               | |
| |  | | ___ _ __ _ __ _  ___ _ __ ___  | | __ _
| |  | |/ _ \ '__| '__| |/ _ \ '__/ _ \ | |/ _` |
| |__| |  __/ |  | |  | |  __/ | |  __/ | | (_| |
|_____/ \___|_|  |_|  |_|\___|_|  \___| |_|\__,_|
                                  | |
        ___ __ _ ___  ___ __ _  __| | ___
       / __/ _` / __|/ __/ _` |/ _` |/ _ \\
      | (_| (_| \__ \ (_| (_| | (_| |  __/
       \___\__,_|___/\___\__,_|\__,_|\___|
"""
FLAG = os.environ.get('FLAG', 'Une erreur est survenue, contactez les admins sur discord.').encode()


class AESCipher:
	@staticmethod
	def pad(message: bytes):
		n = AES.block_size - len(message) % AES.block_size
		return message + bytes([n] * n)
	
	def __init__(self, key: bytes, iv: bytes, mode: int):
		self.key = key
		self.iv = iv
		self.mode = mode

	def encrypt(self, plaintext: bytes) -> str:
		return AES.new(self.key, self.mode, self.iv).encrypt(AESCipher.pad(plaintext + FLAG)).hex()


def main():
	print(BANNER)
	print("Entrez un message en hexadécimal et celui-ci sera bien protégé !""")
	key = os.urandom(16)
	iv = os.urandom(16)
	cipher = AESCipher(key, iv, AES.MODE_CBC)
	while True:
		try:
			plaintext = bytes.fromhex(input('> '))
			print(cipher.encrypt(plaintext))
		except Exception as e:
			print(e)
			print('Une erreur est survenue. Sortie de l\'oracle...')
			break


if __name__ == '__main__':
	main()