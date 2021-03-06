from web3 import Web3
import requests
import random
from cryptography.fernet import Fernet
from flask import Flask, jsonify, request
import json
import hashlib 
import random
import datetime


#Key-1
key = Fernet.generate_key()
fernet = Fernet(key)

#Key-2
key2 = Fernet.generate_key()
fernet2 = Fernet(key2)

 
ciphers = []
decrypted_ciphers = []



app = Flask(__name__)

@app.route('/encrypted',methods = ['POST'])
def encrypted():
    text = request.get_json()
    keys = ['message']
    if not all(key in text for key in keys):
         return "Json key issue!",404
    #Key-1 Encrypted to User message 
    i=0
    enc = None
    enc = fernet.encrypt(text['message'].encode())
    while(True):
        if i==5:
            break
        enc = fernet.encrypt(str(enc).encode())
        i+=1
    
    enc = fernet2.encrypt(str(enc).encode())
    i=0
    while(True):
        if i==5:
            break
        enc = fernet2.encrypt(str(enc).encode())
        i+=1
    
    
    sha = hashlib.sha256(enc).hexdigest()
    ciphers.append(str(enc.decode("utf-8"))+","+str(sha)+","+str(datetime.datetime.now()))
    keys = []
    for i in range(len(ciphers)):
        key = ciphers[i].split(',')
        keys.append(key[1]+","+key[len(key)-1])
    resultCipher = keys[len(keys)-1]
    random.shuffle(keys) #Every request changing the order randomly of keys
    
    response = {'ciphers':resultCipher}    
    return jsonify(response),201
    

@app.route('/decrypted',methods = ['POST'])
def decrypted():
    try:
        
        text = request.get_json()
        keys = ['encrypted']
        if not all(key in text for key in keys):
            return "Json key issue!",404
        #Key-2 Decrypted Key-2 encrypted message
        i=0
        key = text['encrypted']
        cipher = ""
        index =0
        for i in range(len(ciphers)):
            data = ciphers[i].split(',')
            if data[1] == key:
                cipher = data[0]
                index =i
                break
        
        text = bytes(cipher, 'utf-8')
        dec = fernet2.decrypt(text).decode()
        while(True):
            if i ==(5+index):
                break
            dec = dec[1:]
            dec = dec.replace("'",'')
            dec = bytes(dec,'utf-8')  
            dec = fernet2.decrypt(dec).decode()
            i+=1
            
        i=0
        dec = dec[1:]
        dec = dec.replace("'",'')
        dec = bytes(dec,'utf-8')  
        dec = fernet.decrypt(dec).decode()
        while(True):
            if i ==(5):
                break
            dec = dec[1:]
            dec = dec.replace("'",'')
            dec = bytes(dec,'utf-8')  
            dec = fernet.decrypt(dec).decode()
            i+=1
        
    except:
        dec = "Encrypted message is not valid!"
    if dec != "Encrypted message is not valid!":
        decrypted_ciphers.append(key+","+str(datetime.datetime.now()))
        
    result = f'{dec}'
    response = {'result':result}    
    return jsonify(response),201
    

@app.route('/encrypted_data_length',methods = ['GET'])
def encrypted_data_length():
    response = {"total_len":len(ciphers)}
    return jsonify(response),200

@app.route('/decrypted_data_length',methods = ['GET'])
def decrypted_data_length():
    response = {'total_len':len(decrypted_ciphers)}
    return jsonify(response),200
    

@app.route('/last_cipher_time',methods = ['GET'])
def last_cipher_time():
    dates = []
    for i in range(len(ciphers)):
        cipher = ciphers[i].split(',')
        dates.append(cipher[len(cipher)-1])
    
    dates.sort()
    response = {'date':str(dates[len(dates)-1])}
    return jsonify(response),200
        

#I will add remove the key part
@app.route('/remove_key',methods = ['POST'])
def remove_key():
    text = request.get_json()
    json_key = ['key']
    isFoundKey = False
    response = None
    if not all(key in text for key in json_key):
            return "Json key issue!",404
    for i in range(len(ciphers)):
        cipher = ciphers[i].split(',')
        if cipher[len(cipher)-2] == text['key']:
            ciphers.pop(i)
            isFoundKey=True
            break
    index = len(decrypted_ciphers)
    if index > 0:
        while True:
            index-=1
            data = decrypted_ciphers[index].split(',')
            if data[0] == text['key']:
                decrypted_ciphers.pop(index)
                index = len(decrypted_ciphers)
                if index ==0:
                   break
            else:
                 if index == 0:
                   break
            
        
            
    if isFoundKey:
        response = {'result':'Key is successfuly remove!'}
    else:
        response = {'result':'Key is not valid!'}
    
    return jsonify(response),201
        

@app.route('/get_keys',methods = ['GET'])
def get_keys():
    keys = []
    for i in range(len(ciphers)):
        key = ciphers[i].split(',')
        keys.append(key[1]+","+key[2])
    random.shuffle(keys)
    response = {'keys':keys}
    return jsonify(response),200
    
        
@app.route('/encrypted_probability',methods = ['GET'])
def encrypted_probability():
    dates = []
    prob = None
    for i in range(len(ciphers)):
        cipher = ciphers[i].split(',')
        dates.append(cipher[len(cipher)-1])
    dates.sort()
    if len(dates) >=2:
        
        beforeLast = dates[len(dates)-2].split(' ')
        timeBeforeLast = beforeLast[len(beforeLast)-1].split(':')
        last = dates[len(dates)-1].split(' ')
        timeLast = last[len(last)-1].split(':')
        
        hour = float(timeLast[0])-float(timeBeforeLast[0])
        minute = float(timeLast[1])-float(timeBeforeLast[1])
        seconds = float(timeLast[2])-float(timeBeforeLast[2])
        
        if hour < 0:
            hour = hour *-1
        if minute <0:
            minute = minute *-1
        if seconds<0:
            seconds = seconds *-1
        prob = str(hour)+":"+str(minute)+":"+str(seconds)     
        
    response = {'probability':prob}
    return jsonify(response),200



   
app.run(host = '127.0.0.1', port = 5000)

