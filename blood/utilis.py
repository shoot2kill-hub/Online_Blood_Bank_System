import requests




def send_sms(message, phone_number):
    data = {
        'recipients': f'{phone_number}',
        'message': f'{message}',
        'sender': '+250787313298',
    }

    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=('Stephane', 'Stephane2023@23'), verify=False)
    #print(r.json(), r.status_code)
