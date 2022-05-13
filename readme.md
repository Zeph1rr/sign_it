# SIGN IT

## INFO

Version: 1.0.0

Author: Zeph1rr <grianton535@gmail.com>

## INSTALATION

	git clone git@github.com:Zeph1rr/sign_it.git
	cd sign_it
	sudo chmod +x sign_it.sh
	sudo ./sign_it.sh

## USAGE

	sign_it <action> [args]

actions:
- sign: create signature for your file with your private key. Required args: -k (--key), -f (--file)
- verify: verify signature for your file with public key. Required args: -k (--key), -f (--file)
- genkey: generate key pair for your signatures. Args: -p (--path) - path of directory for your key pair. default: ~/
