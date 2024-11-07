import argparse

parser = argparse.ArgumentParser(
                    prog='Keyboard',
                    description='Keyboard encrypt text')

parser.add_argument('text', type=str)
parser.add_argument('offset', type=int)


args = parser.parse_args()


charset1 = "1234567890°+AZERTYUIOP¨£QSDFGHJKLM%µ<WXCVBN?./§"
charset2 = "&é\"'(-è_çà)=azertyuiop^$qsdfghjklmù*<wxcvbn,;:!"
charset3 = "~#{[|`\\^@]}€¤"
charsets = [charset1, charset2, charset3]

def encrypt(text, offset):
	
	encrypted = ""

	for c in text:
		for charset in charsets:
			charset_index = charset.find(c)
			if charset_index > -1:
				off = offset % len(charset)
				index = (charset_index + off) % len(charset)
				encrypted += charset[index]
				break


	return encrypted

print(encrypt(args.text, args.offset))
