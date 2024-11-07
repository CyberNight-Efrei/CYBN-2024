from core import encoder
from core.utils import Encoding, Encryption, Mode, HMAC
from core.helpers import checksum, download_video
from secret import password

file_to_store = 'examples/file.png'
out_dir = 'out'
mode = Mode.BINARY
encoding = Encoding.RES_720_PIX_4
encryption = Encryption.AES


if __name__ == '__main__':
    print('[i] Encoding file')
    encoder.Encoder(
        file_to_store,
        out_dir,
        password=password,
        encoding=encoding,
        mode=mode,
        encryption=encryption
    )
