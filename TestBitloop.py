import requests

def encrypted(message):
    json_data = {'message':message}
    req = requests.post('http://127.0.0.1:5000/encrypted',json=json_data);
    return req.json()

def decrypted(message):
    json_data = {'encrypted':message}
    req = requests.post('http://127.0.0.1:5000/decrypted',json=json_data);
    return req.json()

def remove_key(key):
    json_data = {'key':key}
    req = requests.post('http://127.0.0.1:5000/remove_key',json = json_data);
    return req.json()['result']

def total_cipher():
    req = requests.get('http://127.0.0.1:5000/encrypted_data_length');
    return req.json()['total_len']

def total_decrypted():
    req = requests.get('http://127.0.0.1:5000/decrypted_data_length');
    return req.json()['total_len']

def last_cipher_time():
    req = requests.get('http://127.0.0.1:5000/last_cipher_time');
    return req.json()['date']

def get_keys():
    req = requests.get('http://127.0.0.1:5000/get_keys');
    return req.json()['keys']

def encrypted_probability():
    req = requests.get('http://127.0.0.1:5000/encrypted_probability');
    return req.json()['probability']
    

while True:
    print("'1'=>Encrypted Message")
    print("'2'=>Decrypted Message")
    print("'3'=>Total Encrypted Number")
    print("'4'=>Last Cipher Time")
    print("'5=>Remove Key'")
    print("'6'=>Get Keys")
    print("'7'=>Get Encrypted Probability")
    print("'8'=>Total Decrypted Number")
    print("'9'=>exit")
    
    choice = input("Enter your choice? ")
    if choice == "1":
        message = input("Enter your  message?")
        if message:
            data = encrypted(message)
            print(f"Encrypted data ==> {data['ciphers']}")
           
    if choice == "2":
        message = input("Enter encrypted  message?")
        if message:
            data = decrypted(message)
            print(f"Result => {data['result']}")
    if choice == "3":
        total = total_cipher()
        print(f'Total Cipher ==>  {total}')
    if choice == "4":
        date = last_cipher_time()
        print(f'Last Cipher Time ==>  {date}')
    
    if choice == "5":
        key = input("Enter key Id: ")
        if key:
            result = remove_key(key)
            print(result)
    if choice == "6":
        keys = get_keys()
        for i in range(len(keys)):
            insideKeys = keys[i].split(',')
            print(f"{i+1}.Key: {insideKeys[0]} && Date: {insideKeys[1]}")
    if choice == "7":
        prob = encrypted_probability()
        if prob:
            print(prob)
    
    if choice == "8":
        total = total_decrypted()
        print(f"Total Decrypted Value: {total}")
    
    if choice == "9":
        break
    
    
