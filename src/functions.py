import os
import requests

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from urllib.parse import urlencode


def generate_key_pair(path):
    public_key_path = os.path.join(path, 'sign_key.pub')
    private_key_path = os.path.join(path, 'sign_key')
    private_key = RSA.generate(1024, os.urandom)
    public_key = private_key.publickey()
    with open(private_key_path, 'wb') as file:
        file.write(private_key.exportKey("PEM"))
    with open(public_key_path, 'wb') as file:
        file.write(public_key.exportKey("PEM"))


def get_key_from_yandex(url):
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'

    final_url = base_url + urlencode(dict(public_key=url))
    response = requests.get(final_url)
    download_url = response.json()['href']

    download_response = requests.get(download_url)
    return RSA.import_key(download_response.content)


def get_key_from_file(key_path):
    try:
        with open(key_path, 'r') as file:
            key = RSA.import_key(file.read())
        return key
    except FileNotFoundError:
        return None


def get_key(path):
    return get_key_from_yandex(path) if "https://" in path else get_key_from_file(path)


def get_hash(filename):
    h = SHA256.new()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h


def get_signature(private_key, file_name: str) -> bytes:
    h = get_hash(file_name)
    signature = pkcs1_15.new(private_key).sign(h)
    return signature


def sign(private_key: bytes, file_name: str):
    signature = get_signature(private_key, file_name)
    sign_name = f'{file_name.split(".")[-2].split(os.sep)[-1]}.sig'
    with open(sign_name, 'wb') as file:
        file.write(signature)


def verify_signature(public_key, file_name, signature_path):
    h = get_hash(file_name)
    with open(signature_path, 'rb') as file:
        signature = file.read()
    pkcs1_15.new(public_key).verify(h, signature)

