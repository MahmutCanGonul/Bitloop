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

def last_cipher_time():
    req = requests.get('http://127.0.0.1:5000/last_cipher_time');
    return req.json()['date']

    

while True:
    print("'1'=>Encrypted Message")
    print("'2'=>Decrypted Message")
    print("'3'=>Total Cipher Number")
    print("'4'=>Last Cipher Time")
    print("'5=>Remove Key'")
    print("'6'=>exit")
    
    choice = input("Enter your choice? ")
    if choice == "1":
        message = input("Enter your  message?")
        if message:
            data = encrypted(message)
            for i in range(len(data['ciphers'])):
                print(f"{i+1}==> {data['ciphers'][i]}")
           
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
        break
