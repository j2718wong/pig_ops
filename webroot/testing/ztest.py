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

RANDOM_BOAR_NAMES = ['Berto', 'Kurdapyo', 'KiKoY', 'Didoy', 'Gorio', 'Desidido',
'Ondo', 'Juaning', 'Kokoy', 'Dodo'
]


SAMPLE_CUSTOMIZED_GESTATING_OPS = {
    "name":         "Inject Vitamins",
    "description":  "Inject vitamin Z",
    "num_days_since_insem": 50    
}


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

        print(f'\n\nTesting duplicate account_register; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        assert(res_json['result']['code'] == 'RES_NUM_ACCOUNT_ALREADY_REGISTERED_FOR_USER')
        
        
        
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
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
        
        print(f'\n\nTesting get account user groups; account_id = {account_id}')
        res = model['user_group'].get_user_group_list_by_account(account_id)
        
        print(f'\n\nAccount usergroups; len = {len(res)}')
        pprint.pprint(res)
        assert(len(res) == 4)
        
        
        self.testing_acc_gestating_ops(user_id)
        
        print(f'\n\nTesting get account gestating_ops; account_id = {account_id}')
        res = model['acc_gestating_ops'].get_acc_gestating_ops_list(account_id)
        
        print(f'\n\nAccount gestating_ops; len = {len(res)}')
        pprint.pprint(res)
        assert(len(res) >= 3)
        
        
        
        return {
            'account_id': account_id
        }
        
        
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
            
            result_num  = res_json['result']['num']
            assert(result_num == 0)

            if result_num != 0:
                return
            
            
            is_id_visible = True if 'id' in res_json['pig_farm'] else False
            assert(is_id_visible == False)
            
            
            farm_h_id       = res_json['pig_farm']['h_id']
            res_decrypt     = hashids_common.decrypt(farm_h_id)
            pig_farm_id     = res_decrypt[0]
            
            print(f"created pig_farm_id = {pig_farm_id}")
            assert(pig_farm_id > 0)
            
        
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
        
        url = BASE_URL + 'pig_farm/update'
        
        data = {
            "uhid":         user_uhid,
            "pig_farm_hid": farm_h_id,
            "name":         farm_name + now_ts,
            "adrs_level_1_id": 1,
            "adrs_level_2_id": 2,
            "latitude":     10.262995, 
            "longitude":    123.686722
        }
        
        
        print(f'\n\nTesting farm_update; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        return {
            'pig_farm_id': pig_farm_id
        }
        
        
    def testing_acc_gestating_ops(self, user_id, skip_step = 0):
        user_uhid   = hashids_user.encrypt(user_id)
        
        if skip_step & 0x01 == 0: 
        
            url = BASE_URL + 'acc_gestating_ops/add'
            
            data = {
                "uhid":         user_uhid,
                "name":                 SAMPLE_CUSTOMIZED_GESTATING_OPS['name'],
                "num_days_since_insem": SAMPLE_CUSTOMIZED_GESTATING_OPS['num_days_since_insem'],
                "description":          SAMPLE_CUSTOMIZED_GESTATING_OPS['description']
            }
            
            
            print(f'\n\nTesting adding acc_gestating_ops; url = {url} ; data')
            pprint.pprint(data)
            
            r = requests.post(url, json = data)
            res_text = str(r.text)
            res_json = json.loads(res_text)
            
            print(f"\n\nResult; status_code = {r.status_code}; result")
            pprint.pprint(res_json)
            
            result_num  = res_json['result']['num']
            assert(result_num == 0)

            if result_num != 0:
                return
            
            
            is_id_visible = True if 'id' in res_json['acc_gestating_ops'] else False
            assert(is_id_visible == False)
            
            
            acc_gestating_ops_h_id  = res_json['acc_gestating_ops']['h_id']
            res_decrypt             = hashids_common.decrypt(acc_gestating_ops_h_id)
            acc_gestating_ops_id    = res_decrypt[0]
            
            print(f"acc_gestating_ops_id = {acc_gestating_ops_id}")
            assert(acc_gestating_ops_id > 0)
            
        
        # Test acc_gestating_ops add duplicate
        url = BASE_URL + 'acc_gestating_ops/add'
            
        data = {
            "uhid":                 user_uhid,
            "name":                 SAMPLE_CUSTOMIZED_GESTATING_OPS['name'],
            "num_days_since_insem": SAMPLE_CUSTOMIZED_GESTATING_OPS['num_days_since_insem'],
            "description":          SAMPLE_CUSTOMIZED_GESTATING_OPS['description']
        }
            

        print(f'\n\nTesting duplicate adding acc_gestating_ops; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        
        
        # Test acc_gestating_ops update
        now             = datetime.now()
        now_ts          = now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'acc_gestating_ops/update'
        
        data = {
            "uhid":                 user_uhid,
            "acc_gest_ops_hid":     acc_gestating_ops_h_id,
            "name":                 SAMPLE_CUSTOMIZED_GESTATING_OPS['name'] + now_ts,
            "num_days_since_insem": SAMPLE_CUSTOMIZED_GESTATING_OPS['num_days_since_insem'],
            "description":          SAMPLE_CUSTOMIZED_GESTATING_OPS['description']
        }
        
        
        print(f'\n\nTesting acc_gestating_ops update; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        return {
            'acc_gestating_ops_id': acc_gestating_ops_id
        }
        
        
    def testing_sow_boar_add_multi(self, user_id, pig_farm_id, sex= 'F', num = 3):
        count = 0
        
        while count < num:
            self.testing_sow_boar_add(user_id, pig_farm_id, sex)
            count += 1
    
    
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
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        
        
        len_random_sow_boar_names = len(sow_boar_names)
        
        sow_boar_list = res_json['data']
        len_items = len(sow_boar_list)
        
        if len_items == 0:
            sow_boar_number = random.randint(10000, 20000)
            
            index           = random.randint(0, len_random_sow_boar_names-1)
            sow_boar_name   = sow_boar_names[index]
            
                    
        else:
            
            taken_sow_boar_names = []
            for cur_entry in sow_boar_list:
                taken_sow_boar_names.append(cur_entry['name'])
            
            last_entry = sow_boar_list[len_items -1]
            last_number = int(last_entry['number'])
            
            sow_boar_number = last_number + random.randint(1, 20)
            
            
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
          "number": str(sow_boar_number),
          "name": sow_boar_name,
          "date_of_birth": dt_dob_s
        }
        
        url = BASE_URL + 'sow_boar/add'
        
        print(f'\n\nTesting adding sow_boar entry; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code} ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
        sow_boar_id = res_json['sow_boar']['id']
        
        
        # Test sow boar update
        now             = datetime.now()
        now_ts          = now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'sow_boar/update'
        
        new_name        = sow_boar_name + now_ts
        new_name        = new_name[0:20]
        
        data = {
            "uhid": user_uhid,
            "sow_boar_id": sow_boar_id,
            
            
            "number":   str(sow_boar_number),
            "name":     new_name,
            "notes":    "Updated sow boar"
            
        }
        
        
        print(f'\n\nTesting sow_boar_update; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
    def test_auto_clean_data(self, user_id, acc_name, farm_name):
        self.test_account_register(user_id, acc_name)
        
       
        res_pig_farm = self.testing_pig_farm(user_id, farm_name)
        
        pig_farm_id = res_pig_farm['pig_farm_id']
        self.testing_sow_boar_add_multi(user_id, pig_farm_id, sex= 'F', num = 10)
        self.testing_sow_boar_add_multi(user_id, pig_farm_id, sex= 'M', num = 2)