from flask import Flask, redirect
from flask import render_template, request
from stellar_base.keypair import Keypair
import json
import requests

app = Flask(__name__)

@app.route("/gen_address")
def gen_address():
    kp = Keypair.random()
    publickey = kp.address().decode()
    seed = kp.seed().decode()
    return json.dumps({'publickey': publickey, 'seed': seed})    

def fund_account(address):
    r = requests.get('https://horizon-testnet.stellar.org/friendbot?addr=' + address)
    return r.text


if __name__ == '__main__':
    ISSUER_ADDRESS = 'GDKQWW4VYWIPWRGDFZO2DDMX7NNVCSB2T6AWFNT72XHMYZACAUYFGW66'
    ISSUER_SEED = 'SAKIXIIAMGLKGZF2BSRUJHNE5ZAP6X7UWIUWCGU3LKP6CDRAJW7DFCNK'
    result = fund_account(ISSUER_ADDRESS)