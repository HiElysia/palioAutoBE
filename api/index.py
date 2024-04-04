
import json

import requests

from flask import Flask,request,jsonify
from flask_cors import CORS


app = Flask(__name__)

cors = CORS(app,resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/login_info')
def login_info():
    wallet_address = request.args.get('address','')
    url = 'https://api.xter.io/account/v1/login/wallet/%s' % (wallet_address.upper())
    resp = requests.get(url,timeout=3)
    data = json.loads(resp.text)

    return jsonify({'data':data['data'].get('message','')})

@app.route('/login')
def login():
    wallet_address = request.args.get('address','')
    wallet_sign = request.args.get('sign','')
    url = 'https://api.xter.io/account/v1/login/wallet'
    resp = requests.post(url,json={
        'address':wallet_address.upper(),
        'type':'eth',
        'sign':wallet_sign,
        'provider':'METAMASK',
        'invite_code':''
    },timeout=3)
    data = json.loads(resp.text)

    return jsonify({'data':data['data'].get('id_token','')})

@app.route('/get_point')
def get_point():
    wallet_address = request.args.get('address','')
    auth_token = request.args.get('auth_token','')
    url = 'https://api.xter.io/palio/v1/user/%s/point' % (wallet_address)
    resp = requests.get(url,headers={'Authorization': auth_token,},timeout=10)
    data = json.loads(resp.text)

    return jsonify({'data':data.get('data',{})})

@app.route('/egg_eat')
def egg_eat():
    wallet_address = request.args.get('address','')
    auth_token = request.args.get('auth_token','')
    prop_id = int(request.args.get('prop',1))
    url = 'https://api.xter.io/palio/v1/user/%s/prop' % (wallet_address)
    resp = requests.post(url,headers={
        'Authorization': auth_token,
    },json={'prop_id':prop_id},timeout=3)
    data = json.loads(resp.text)

    if not data.get('err_code',0):
        return jsonify({'data':1})
    
    return jsonify({'data':0})

