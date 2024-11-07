from enum import Enum
import os
from Crypto.Cipher import AES

from core.exceptions import EncryptionException


class _Encoding:
    def __init__(self, width: int, height: int, square_size: int) -> None:
        self.width = width
        self.height = height
        self.square_size = square_size


class Encoding(Enum):
    RES_720_PIX_2 = 0, _Encoding(1280, 720, 2)
    RES_720_PIX_4 = 1, _Encoding(1280, 720, 4)
    RES_720_PIX_8 = 2, _Encoding(1280, 720, 8)
    RES_720_PIX_16 = 3, _Encoding(1280, 720, 16)
    RES_1080_PIX_2 = 4, _Encoding(1920, 1080, 2)
    RES_1080_PIX_4 = 5, _Encoding(1920, 1080, 4)
    RES_1080_PIX_8 = 6, _Encoding(1920, 1080, 8)
    
    def __init__(self, _id: int, _info: str) -> None:
        self.id = _id
        self.info = _info
    
    @classmethod
    def _missing_(cls, value: any) -> 'Encoding':
        for item in cls:
            if value in item.value:
                return item
        return super()._missing_(value)


class _Mode:
    def __init__(self, channels: int) -> None:
        self.channels = channels


class Mode(Enum):
    BINARY = 0, _Mode(1)
    
    def __init__(self, _id: int, _info: str) -> None:
        self.id = _id
        self.info = _info
    
    @classmethod
    def _missing_(cls, value: any) -> 'Mode':
        for item in cls:
            if value in item.value:
                return item
        return super()._missing_(value)


class Chunk(Enum):
    FHDR = b'FHDR'
    FDAT = b'FDAT'
    FEND = b'FEND'


class Encryption(Enum):
    NONE = 0
    AES  = 1


class HMAC(Enum):
    NONE     = 0, 'none'
    BLAKE2B  = 1, 'blake2b'
    BLAKE2S  = 2, 'blake2s'
    MD5      = 3, 'md5'
    SHA1     = 4, 'sha1'
    SHA224   = 5, 'sha224'
    SHA256   = 6, 'sha256'
    SHA384   = 7, 'sha384'
    SHA512   = 8, 'sha512'
    SHA3_224 = 9, 'sha3_224'
    SHA3_256 = 10, 'sha3_256'
    SHA3_384 = 11, 'sha3_384'
    SHA3_512 = 12, 'sha3_512'
    
    def __init__(self, _id: int, _hash: str) -> None:
        self.id = _id
        self.hash = _hash
    
    @classmethod
    def _missing_(cls, value: any) -> 'HMAC':
        for item in cls:
            if value in item.value:
                return item
        return super()._missing_(value)


class FHDR:
    DEFAULT_HMAC = HMAC.SHA256
    DEFAULT_ITERATIONS = 1024
    
    LEN_ENCRYPTION = 1
    LEN_IV = 16
    LEN_HMAC = 1
    LEN_SALT = 16
    LEN_ITERATIONS = 4
    
    @staticmethod
    def parse(data: bytes) -> 'FHDR':
        i = 0
        
        j = i + FHDR.LEN_ENCRYPTION
        encryption = Encryption(int.from_bytes(data[i:j], 'big'))
        i = j
        
        j = i + FHDR.LEN_IV
        if encryption == Encryption.NONE:
            iv = data[i:j]
        elif encryption == Encryption.AES:
            iv = data[i:j][:AES.block_size]
        i = j
        
        j = i + FHDR.LEN_HMAC
        hmac = HMAC(int.from_bytes(data[i:j], 'big'))
        i = j
        
        j = i + FHDR.LEN_SALT
        salt = data[i:j]
        i = j
        
        j = i + FHDR.LEN_ITERATIONS
        iterations = int.from_bytes(data[i:j], 'big')
        i = j
        
        return FHDR(encryption, iv, hmac, salt, iterations)
        
    def __init__(
            self,
            encryption: Encryption,
            iv: bytes = b'\x00' * LEN_IV,
            hmac: HMAC = HMAC.NONE,
            salt: bytes = b'\x00' * LEN_SALT,
            iterations: int = 0
        ):
        
        if encryption == Encryption.NONE:
            pass
        elif encryption == Encryption.AES:
            iv = os.urandom(AES.block_size) if iv is None else iv
        else:
            raise EncryptionException(f'Encryption {encryption.name} is not implemented.')
            
        if len(iv) > FHDR.LEN_IV:
            raise EncryptionException(f'IV is too long ({FHDR.LEN_IV} maximum), {len(iv)} provided.')
        if len(salt) != FHDR.LEN_SALT:
            raise EncryptionException(f'Salt must be {FHDR.LEN_SALT} bytes long, {len(salt)} provided.')
        if iterations > 0x100**FHDR.LEN_ITERATIONS - 1:
            raise EncryptionException(f'Iterations max : {0x100**FHDR.LEN_ITERATIONS - 1}, {iterations} provided.')
        
        self.encryption = encryption
        self.iv = iv
        self.hmac = hmac
        self.salt = salt
        self.iterations = iterations
    
    def encode(self) -> bytes:        
        data = b''
        data += self.encryption.value.to_bytes(FHDR.LEN_ENCRYPTION, 'big')
        data += self.iv.ljust(FHDR.LEN_IV, b'\x00')
        data += self.hmac.id.to_bytes(FHDR.LEN_HMAC, 'big')
        data += self.salt
        data += self.iterations.to_bytes(FHDR.LEN_ITERATIONS, 'big')
        return data