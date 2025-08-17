# August 17, 2025
# Jack Wong

import sys

from datetime               import datetime

sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import requests
import json
import pprint

BASE_URL = 'http://localhost:8080/'

RANDOM_NAMES = [
('Albert',      'Pablo',        'aPablo@gmail.com'),
('Fergus',      'Laurente',     'fLaurente@gmail.com'),
('Daniel',      'Guzman',       'dGuzman@gmail.com'),
('Elton',       'Rico',         'eRico@gmail.com'),
('Arvin',       'dela Cruz',    'adelaCruz@gmail.com'),
('Ernie',       'Sotto',        'eSotto@gmail.com'),
('Jacob',       'Vasquez',      'jVasquez@gmail.com'),
('Jerome',      'Gregorio',     'jGregorio@gmail.com'),
('Christian',   'Guillermo',    'cGuillermo@gmail.com'),
('Genkei',      'Javier',       'gJavier@gmail.com')]


class TestAPIUser:
    def test_register(self):
        test = 1

class TestAPIAccount:
    
    def test_account_register(self, user_id, acc_name, skip_step = 0):
        user_uhid   = hashids_user.encrypt(user_id)
        
        if skip_step & 0x01 == 0: 
        
            url = BASE_URL + 'account/register'
            
            data = {
                "uhid":         user_uhid,
                "name":         acc_name,
                "country_id":   1
            }
            
            
            print(f'\n\nTesting adding account_register; url = {url} ; data')
            pprint.pprint(data)
            
            r = requests.post(url, json = data)
            
            print(f"\n\nResult; status_code = {r.status_code}")
            
            result = str(r.text)
            print(result)
            
            res = json.loads(result)
            
            
            if res['result']['num'] != 0:
                return
            
        
        # Test account register duplicate
        url = BASE_URL + 'account/register'
            
        data = {
            "uhid":         user_uhid,
            "name":         acc_name,
            "country_id":   1
        }

        print(f'\n\nTesting duplicate adding account_register; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        
        print(f"\n\nResult; status_code = {r.status_code}")
        
        result = str(r.text)
        print(result)
        
        res = json.loads(result)
        
        
        # Test account update
        account_h_id = res['account']['h_id']
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'account/update'
        
        data = {
            "uhid":         user_uhid,
            "name":         acc_name + now_ts
        }
        
        
        print(f'\n\nTesting account_update; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        
        print(f"\n\nResult; status_code = {r.status_code}")
        
        result = str(r.text)
        print(result)
        
        
    def testing_pig_farm(self, user_id, farm_name, skip_step = 0):
        user_uhid   = hashids_user.encrypt(user_id)
        
        if skip_step & 0x01 == 0: 
        
            url = BASE_URL + 'pig_farm/add'
            
            data = {
                "uhid":         user_uhid,
                "name":         farm_name
            }
            
            
            print(f'\n\nTesting adding pig_farm; url = {url} ; data')
            pprint.pprint(data)
            
            r = requests.post(url, json = data)
            
            print(f"\n\nResult; status_code = {r.status_code}")
            
            result = str(r.text)
            print(result)
            
            res = json.loads(result)
            
            
            if res['result']['num'] != 0:
                return
            
        
        # Test account register duplicate
        url = BASE_URL + 'pig_farm/add'
            
        data = {
            "uhid":         user_uhid,
            "name":         farm_name
        }

        print(f'\n\nTesting duplicate adding pig_farm; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        
        print(f"\n\nResult; status_code = {r.status_code}")
        
        result = str(r.text)
        print(result)
        
        res = json.loads(result)
        
        