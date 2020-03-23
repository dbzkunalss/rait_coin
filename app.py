from flask import Flask, redirect
from flask import render_template, request
from stellar_base.keypair import Keypair
import json

@app.route("/gen_address")
def gen_address():
    kp = Keypair.random()
    publickey = kp.address().decode()
    seed = kp.seed().decode()
    return json.dumps({'publickey': publickey, 'seed': seed})