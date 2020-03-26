from flask import Flask, redirect
from flask import render_template, request
from stellar_base.keypair import Keypair
from stellar_base.asset import Asset
from stellar_base.horizon import horizon_testnet
from stellar_base.operation import ChangeTrust

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


def create_asset(code, issuer_address):
    asset = Asset(code, issuer_address)
    return asset

def connect_horizon():
    horizon = horizon_testnet()
    return horizon

def opr_change_trust(asset_object, receiver_address, receiver_seed, horizon):

    op = ChangeTrust({
        'source': receiver_address,
        'asset': asset_object,
        'limit': '5000'
    })

    sequence = horizon.account(receiver_address).get('sequence')
    print(sequence)

if __name__ == '__main__':
    ISSUER_ADDRESS = 'GDKQWW4VYWIPWRGDFZO2DDMX7NNVCSB2T6AWFNT72XHMYZACAUYFGW66'
    ISSUER_SEED = 'SAKIXIIAMGLKGZF2BSRUJHNE5ZAP6X7UWIUWCGU3LKP6CDRAJW7DFCNK'
    # result = fund_account(ISSUER_ADDRESS)
    ASSET_CODE = 'RAITCOIN'
    CUSTOMER_ADDRESS = 'GDTZPBMS6FK7BLNOLTW5CLKLP2YOVWBX5S5P46HFVLRBASI34QMBN45F'
    CUSTOMER_SEED = 'SDOWS44HIDFFNTOBDRL3OENAVKK7PW5AY3AUC4C2BYPZBWR5DZ2NSND2'
    new_asset = create_asset(ASSET_CODE,ISSUER_ADDRESS)
    result = fund_account(CUSTOMER_ADDRESS)
    horizon = connect_horizon()
    opr_change_trust(new_asset,CUSTOMER_ADDRESS,CUSTOMER_SEED, horizon)
    