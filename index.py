#!/usr/bin/python
from flask import Flask, render_template, redirect, url_for, request
import requests
import json
app = Flask(__name__)

@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/oauth')
def oauth():
    code = str(request.args.get('code'))
    resToken = getAccessToken("e3b2afd2e5216a12322064d69b530dfa",str(code))  #XXXXXXXXX 자리에 RESET API KEY값을 사용
    return 'code=' + str(code) + '<br/>response for token=' + str(resToken)

def getAccessToken(clientId, code) :  # 세션 코드값 code 를 이용해서 ACESS TOKEN과 REFRESH TOKEN을 발급 받음
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code"
    payload += "&client_id=" + clientId
    payload += "&redirect_url=http%3A%2F%2Flocalhost%3A5000%2Foauth&code=" + code
    headers = {
        'Content-Type' : "application/x-www-form-urlencoded",
        'Cache-Control' : "no-cache",
    }
    reponse = requests.request("POST",url,data=payload, headers=headers)
    access_token = json.loads(((reponse.text).encode('utf-8')))
    return access_token

if __name__ == '__main__' :
    app.run(debug = True)

