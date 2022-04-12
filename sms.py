import requests
import os
import logging
from dotenv import load_dotenv
load_dotenv()

log = logging.getLogger(__name__)


token = os.getenv("token")
sms_from_id = os.getenv("sms_from_id")

def send_SMS(to_number: str, message_content: str, from_number: str = sms_from_id):
    """ Send SMS via IMI Sandbox """
    headers = {'Content-Type': 'application/json', 'Authorization': token}
    url = 'https://api-sandbox.imiconnect.io/v1/sms/messages'
    payload = {
        'from': from_number, 
        'to': to_number, 
        'content': message_content,
        'contentType': 'TEXT'
    }
    response = requests.post(url=url, json=payload, headers=headers)
    if response.status_code == 202:
        log.info(f'Successfully sent SMS to: {to_number}')
        return "SMS Success"
    else:
        log.info(f'Failed to send SMS to: {to_number}')
        print(response.text)
        return "SMS Failure"