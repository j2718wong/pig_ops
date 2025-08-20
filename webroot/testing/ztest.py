# August 17, 2025
# Jack Wong

import sys


from datetime               import datetime, timedelta

sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import requests
import random
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


RANDOM_SOW_NAMES = [
'Soling', 'Sita', 'Kurdapya', 'Imyat', 'Tasing', 'Narsing', 'Medi', 
'Segunda', 'Berta', 'Osang', 'Petra',  'Nitang'  'Menang', 'Adela',
'Linda', 'Kikay', 'Diday'

]

RANDOM_BOAR_NAMES = ['Berto', 'Kurdapyo', 'KiKoY', 'Didoy', 'Gorio', 'Desidido'
'Ondo', 'Juaning', 'Kokoy'
]



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
            res_text = str(r.text)
            res_json = json.loads(res_text)
        
            print(f"\n\nResult; status_code = {r.status_code}; result =")
            pprint.pprint(res_json)
            
            result_num  = res_json['result']['num']
            assert(result_num == 0)
            
            if result_num != 0:
                return
            
            
            account_h_id    = res_json['account']['h_id']
            res_decrypt     = hashids_account.decrypt(account_h_id)
            account_id      = res_decrypt[0]
        
            print(f"created account_id = {account_id}")
            
            assert(account_id > 0)
            
        
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
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        
        
        # Test account update
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
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        
        print(f'\n\nTesting get account user groups; account_id = {account_id}')
        res = model['user_group'].get_user_group_list_by_account(account_id)
        
        print(f'\n\nAccount usergroups; len = {len(res)}')
        pprint.pprint(res)
        
        
        print(f'\n\nTesting get account gestating_ops; account_id = {account_id}')
        res = model['acc_gestating_ops'].get_account_gestating_ops_list(account_id)
        
        print(f'\n\nAccount gestating_ops; len = {len(res)}')
        pprint.pprint(res)
        
        
        
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
            res_text = str(r.text)
            res_json = json.loads(res_text)
            
            print(f"\n\nResult; status_code = {r.status_code}; result")
            pprint.pprint(res_json)
            

            if res_json['result']['num'] != 0:
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
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        
        
        # Test farm update
        now             = datetime.now()
        now_ts          = now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'account/update'
        
        data = {
            "uhid":         user_uhid,
            "name":         farm_name + now_ts,
            "adrs_level_1_id": 1,
            "adrs_level_2_id": 2,
            "latitude":     10.262995, 
            "longitude":    123.686722
        }
        
        
        print(f'\n\nTesting account_update; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
    
    def testing_sow_boar_add(self, user_id, pig_farm_id, sex= 'F'):
        user_uhid   = hashids_user.encrypt(user_id)
        pfhid       = hashids_common.encrypt(pig_farm_id)
        
        # Get sow list first for pig farm_name
        if sex =='F':
            sow_boar_names = RANDOM_SOW_NAMES
            url = BASE_URL + 'sow_boar/list?pfhid=' + pfhid + '&sex=F'
        else:
            sow_boar_names = RANDOM_BOAR_NAMES
            url = BASE_URL + 'sow_boar/list?pfhid=' + pfhid + '&sex=M'
        
        r = requests.get(url)
        
        print(f"\n\nResult; status_code = {r.status_code}")
        
        result = str(r.text)
        print(result)
        
        res = json.loads(result)
        
        len_random_sow_boar_names = len(sow_boar_names)
        
        sow_boar_list = res['data']
        len_items = len(sow_boar_list)
        
        if len_items == 0:
            number = random.randint(10000, 20000)
            
            index           = random.randint(0, len_random_sow_boar_names-1)
            sow_boar_name   = sow_boar_names[index]
            
                    
        else:
            
            taken_sow_boar_names = []
            for cur_entry in sow_boar_list:
                taken_sow_boar_names.append(cur_entry['name'])
            
            last_entry = sow_boar_list[len_items -1]
            last_number = int(last_entry['number'])
            
            number = last_number + random.randint(1, 20)
            
            
            len_taken_sow_boar_names = len(taken_sow_boar_names)
            
            if len_taken_sow_boar_names < len_random_sow_boar_names:
            
                while True:
                    index           = random.randint(0, len_random_sow_boar_names-1)
                    sow_boar_name   = sow_boar_names[index]
                    
                    if sow_boar_name not in taken_sow_boar_names:
                        break
                        
            else:
                index           = random.randint(0, len_random_sow_boar_names-1)
                sow_boar_name   = sow_boar_names[index]
                    
        
        now         = datetime.now()
        
        random_num_days = random.randint(0, 60)
        dt_dob      = now - timedelta(days = (210 + random_num_days))
        dt_dob_s    = now.strftime('%Y-%m-%d')
        
        data = {
          "uhid": user_uhid,
          "pfhid": pfhid,
          
          "sow_status_id": 2,
          "sex": sex,
          "number": str(number),
          "name": sow_boar_name,
          "date_of_birth": dt_dob_s
        }
        
        url = BASE_URL + 'sow_boar/add'
        
        print(f'\n\nTesting adding sow_boar entry; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        
        print(f"\n\nResult; status_code = {r.status_code}")
        
        result = str(r.text)
        print(result)
        
        
        
  