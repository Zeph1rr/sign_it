# SIGN IT



## INFO

- Version: 1.0.0
- Python: 3.10.x

Author: Zeph1rr <grianton535@gmail.com>

## INSTALATION

	git clone https://github.com/Zeph1rr/sign_it.git

## USAGE

	cd src
    python ./main.py -a <action> [args]

To find out all the available arguments use
    
    python ./main.py -h

actions:
- sign: create signature for your file with your private key. Required args: -k (--key), -f (--file)
- verify: verify signature for your file with public key. Required args: -k (--key), -f (--file), -s (--signature)
- genkey: generate key pair for your signatures. Args: -p (--path) - path of directory for your key pair. default: ~/sign_keys
