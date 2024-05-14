import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class MpesaC2bCredential:
    consumer_key = 'ZA9Qkfqguoq0iJtVkmAny1d9uE5P5mYRl2MnJT5SnA5E5ABo'
    consumer_secret = '6mDMlj5vpbdj7OCekSmXFjJOWCzDPN4KsGa4KNPANlxXVLqTYaVmNzVGIsgJGGKS'
    api_URL = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]


class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "4026345"
    OffSetValue = '0'
    passkey = '9d782d48aaaa5aef715853e5c099b2036cf76c7fbcbb8978bb986963116d98dc'

    data_to_encode = Business_short_code + passkey + lipa_time

    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')
