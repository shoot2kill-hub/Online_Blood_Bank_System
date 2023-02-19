import requests

email_user = ''
password_user = ''


def send_sms(message, phone_number):
    data = {
        'recipients': f'{phone_number}',
        'message': f'{message}',
        'sender': '+250786405263',
    }

    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=(f'{email_user}', f'{password_user}'), verify=False)
    # print(r.json(), r.status_code)
