import requests

email_user = 'guystephane78@gmail.com'
password_user = 'Stephane2023@23'


def send_sms(message, phone_number):
    data = {
        'recipients': f'{phone_number}',
        'message': f'{message}',
        'sender': '0787313298',
    }

    r = requests.post('https://www.intouchsms.co.rw/api/sendsms/.json', data,
                      auth=(f'guystephane78@gmail.com', f'Stephane2023@23'))
    print(r.json(), r.status_code)
