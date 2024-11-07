import os
import zipfile
import numpy as np
import numpy.typing as npt
from hashlib import md5, pbkdf2_hmac
from pytubefix import YouTube
from core.utils import FHDR


def int2bits(n: int, size: int) -> npt.NDArray[np.uint8]:
    return np.unpackbits(np.frombuffer((n & (256**size - 1)).to_bytes(size, 'big'), np.uint8))


def bytes2bits(data: bytes | bytearray) -> npt.NDArray[np.uint8]:
    return np.unpackbits(np.frombuffer(data, np.uint8))


def checksum(filepath: str) -> bytes:
    with open(filepath, 'rb') as f:
        h = md5(f.read())
    return h.digest()


def generate_key(password: bytes, fhdr: FHDR) -> bytes:
    return pbkdf2_hmac(fhdr.hmac.hash, password, fhdr.salt, fhdr.iterations, 32)


def download_video(youtube_code: str, file_out: str) -> None:
    yt = YouTube(f'http://youtube.com/watch?v={youtube_code}')
    video = yt.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
    os.makedirs(os.path.dirname(file_out), exist_ok=True)
    
    print(f'[i] Downloading video')
    video.download(filename=file_out)


def zip(filepath: str, out: str) -> None:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zip:
        zip.write(filepath, os.path.basename(filepath))


def unzip(filepath: str, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(filepath, 'r') as zip:
        return zip.extract(zip.filelist[0], out_dir)


def clear_tmp(tmp_dir: str = 'tmp') -> None:
    if len(os.listdir(tmp_dir)) == 0:
        os.rmdir(tmp_dir)