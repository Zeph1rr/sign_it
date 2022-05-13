#!/bin/bash

apt update && apt install python3 python3-pip

pip3 install -r requirements.txt

echo '#!/usr/bin/python3' > /usr/bin/sign_it

cat main.py >> /usr/bin/sign_it

chmod +x /usr/bin/sign_it