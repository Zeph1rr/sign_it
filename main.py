import os
import argparse
import requests
import sys

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from urllib.parse import urlencode


actions = [
    'sign',
    'verify',
    'genkey'
]


def generate_key_pair(path):
    public_key_path = os.path.join(path, 'sign_key.pub')
    private_key_path = os.path.join(path, 'sign_key')
    private_key = RSA.generate(1024, os.urandom)
    public_key = private_key.publickey()
    with open(private_key_path, 'wb') as file:
        file.write(private_key.exportKey("PEM"))
    with open(public_key_path, 'wb') as file:
        file.write(public_key.exportKey("PEM"))
    print("=" * 5 + "SUCCESSFULLY CREATED" + "=" * 5)


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
        print("No such file with key")
        return


def get_hash(filename):
    h = SHA256.new()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h


def sign(private_key, file_name):
    h = get_hash(file_name)
    signature = pkcs1_15.new(private_key).sign(h)
    return signature


def verify(public_key, file_name, signature):
    h = get_hash(file_name)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        print("=" * 5 + "SUCCESSFULLY VERIFIED" + "=" * 5)
    except ValueError:
        print("=" * 5 + "ERROR, INVALID SIGNATURE" + "=" * 5)


def main():
    parser = argparse.ArgumentParser(description='Sign document or verify the sign')
    parser.add_argument('action', nargs='?', help='Action to do (sign/verify/genkey)')
    parser.add_argument('-k', '--key', required=False, help='Path to key file')
    parser.add_argument('-f', '--file', required=False, help='Path to file')
    parser.add_argument('-p', '--path', required=False, help='Path to directory for keys')
    if len(sys.argv) < 2:
        print("=" * 5 + "EXPECTED SOME ARGUMENTS" + "=" * 5)
        return
    args = parser.parse_args()
    action = args.action.lower()
    if actions.index(action) < 2:
        key = get_key_from_yandex(args.key) if "https://" in args.key else get_key_from_file(args.key)
    if action not in actions:
        print("=" * 5 + "UNKNOWN ACTION" + "=" * 5)
        return
    if action == 'sign':
        try:
            file_name = args.file
            signature = sign(key, file_name)
            with open(file_name, 'rb') as file:
                content = file.read()
            with open(file_name, 'wb') as file:
                file.write(content + signature)
            print("=" * 5 + "SUCCESSFULLY SIGNED" + "=" * 5)
        except FileNotFoundError:
            print("No such file")
            return
    elif action == 'verify':
        try:
            file_name = args.file
            with open(file_name, 'rb') as file:
                content = file.read()
                with open("temp.docx", 'wb') as temp_file:
                    temp_file.write(content[:-128])
                signature = content[-128:]
            verify(key, "temp.docx", signature)
            os.remove("temp.docx")
        except FileNotFoundError:
            print("No such file")
            return
    elif action == 'genkey':
        path = args.path if args.path else os.path.join(os.environ['HOME'], 'sign_keys')
        try:
            generate_key_pair(path)
        except FileNotFoundError:
            os.makedirs(path)
            generate_key_pair(path)


if __name__ == "__main__":
    main()
