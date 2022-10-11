import argparse
from os import path, makedirs, environ
from datetime import date
from loguru import logger

from errors import *
from functions import get_key, sign, generate_key_pair, verify_signature


def main():
    logger.add(f"debug_{date.today()}.log", format="{time} {level} {message}", level="DEBUG", rotation="1 day")

    parser = argparse.ArgumentParser(description='Sign document or verify the sign')
    parser.add_argument('-a', '--action', required=True, help='Action to do (sign/verify/genkey)')
    parser.add_argument('-k', '--key', required=False, help='Path or link to key file')
    parser.add_argument('-f', '--file', required=False, help='Path to file')
    parser.add_argument('-s', '--signature', required=False, help='Path to signature')
    parser.add_argument('-p', '--path', required=False, help='Path to directory for keys')
    args = parser.parse_args()
    action = args.action

    if args.key:
        key = get_key(args.key)
        if key is None:
            logger.error("No such file with key")
            return

    match action:
        case "genkey":
            key_path = args.path if args.path else path.join(environ['HOME'], 'sign_keys')
            try:
                generate_key_pair(key_path)
                logger.success("Successfully created")
            except FileNotFoundError:
                makedirs(key_path)
                generate_key_pair(key_path)
            except Exception as ex:
                logger.error(ex)
        case "sign":
            file_name = args.file
            private_key = get_key(args.key)
            sign(private_key, file_name)
            logger.success("Successfully signed")
        case "verify":
            file_name = args.file
            public_key = get_key(args.key)
            signature = args.signature
            verify_signature(public_key, file_name, signature)
            logger.success("Successfully verified")
        case _:
            raise UnavailableActionError("Unavailable action! (sign/verify/genkey)")


if __name__ == "__main__":
    try:
        main()
    except ValueError as ex:
        logger.error(ex)
    except Exception as ex:
        logger.error(ex)
