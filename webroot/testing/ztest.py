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
'Segunda', 'Berta', 'Osang', 'Petra',  'Nitang',  'Menang', 'Adela',
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

SAMPLE_PIG_RACE_LINE = {
    "name":         "Camborough 48",
    "description":  "PIC camborough 48"
}



class TestAPIUser:
    def test_register(self):
        test = 1



class TestAPIAccount:
    
    def test_account_register(self, user_id, acc_name, skip_step = 0):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f'\n\n#################  {now_ts}  #####################################################################')
        
        
        if skip_step & 0x01 == 0: 
            url = BASE_URL + 'account/register'
            
            data = {
                "uhid":         user_uhid,
                "name":         acc_name,
                "country_id":   1
            }
            
            
            print(f'***** Testing adding account_register; url = {url} ; data')
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
            
            
            account_hid    = res_json['account']['hid']
            res_decrypt     = hashids_account.decrypt(account_hid)
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

        print(f'\n\n*****  Testing duplicate account_register; url = {url} ; data')
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
        
        
        print(f'\n\n***** Testing account_update; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
        
        print(f'\n\n***** Testing get account user groups; account_id = {account_id}')
        res = model['user_group'].get_user_group_list_by_account(account_id)
        
        print(f'\n\nAccount usergroups; len = {len(res)}')
        pprint.pprint(res)
        assert(len(res) == 4)
        
        
        self.test_acc_gestating_ops(user_id)
        
        print(f'\n\n***** Testing get account gestating_ops; account_id = {account_id}')
        res = model['acc_gestating_ops'].get_list(account_id)
        
        print(f'\n\nAccount gestating_ops; len = {len(res)}')
        pprint.pprint(res)
        assert(len(res) >= 3)
        
        
        self.test_pig_race_line(user_id, account_hid)
        
        self.test_semen_supplier(user_id)
        
        self.test_feed_brand(user_id)
        
        self.test_feed_supplier(user_id)
        
        return {
            'account_id':       account_id,
            'account_hid':     account_hid,
        }
        
        
    def test_semen_supplier(self, user_id):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f'\n\n#################  {now_ts}  #####################################################################')
        
        url = BASE_URL + 'semen_supplier/add'
            
        data = {
            "uhid":         user_uhid,
            "name":                 'Growbest Agrivet',
            "address_level_1_id":   1,
            "address_level_2_id":   1
        }
        

        print(f'***** Testing adding semen_supplier; url = {url} ; data')
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
        
    
        # Test get_list semen_supplier
        url = BASE_URL + 'semen_supplier/list?inc_deleted=1&inc_user_audit=1'
        
        print(f'\n\n****** Testing semen_supplier get_list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        len_items = len(res_json['data'])
        assert(len_items > 0)
        
    
    def test_feed_brand(self, user_id):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f'\n\n#################  {now_ts}  #####################################################################')
        
        url = BASE_URL + 'feed_brand/add'
            
        data = {
            "uhid":         user_uhid,
            "name":         'Promix',
        }
        

        print(f'***** Testing adding feed_brand; url = {url} ; data')
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
        
        
        url = BASE_URL + 'feed_brand/add'
            
        data = {
            "uhid":         user_uhid,
            "name":         'Ultrapack',
        }
        

        print(f'***** Testing adding feed_brand; url = {url} ; data')
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
        
        
        
        
        # Test get_list feed_brand
        url = BASE_URL + 'feed_brand/list?inc_deleted=1&inc_user_audit=1'
        
        print(f'\n\n****** Testing pig_race_line get_list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
    
        len_items = len(res_json['data'])
        assert(len_items > 0)
    
    
    def test_feed_supplier(self, user_id):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f'\n\n#################  {now_ts}  #####################################################################')
        
        url = BASE_URL + 'feed_supplier/add'
            
        data = {
            "uhid":         user_uhid,
            "name":         'Ayan Sampan',
            "address_level_1_id":   1,
            "address_level_2_id":   1
        }
        

        print(f'***** Testing adding feed_supplier; url = {url} ; data')
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
        
    
        # Test get_list feed_supplier
        url = BASE_URL + 'feed_supplier/list?inc_deleted=1&inc_user_audit=1'
        
        print(f'\n\n****** Testing pig_race_line get_list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
    
        len_items = len(res_json['data'])
        assert(len_items > 0)
    
        
    def test_pig_farm(self, user_id, farm_name, skip_step = 0):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f'\n\n#################  {now_ts}  #####################################################################')
        
        
        if skip_step & 0x01 == 0: 
        
            url = BASE_URL + 'pig_farm/add'
            
            data = {
                "uhid":         user_uhid,
                "name":         farm_name
            }
            
            
            print(f'*****  Testing adding pig_farm; url = {url} ; data')
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
            
            
            farm_hid       = res_json['pig_farm']['hid']
            res_decrypt     = hashids_common.decrypt(farm_hid)
            pig_farm_id     = res_decrypt[0]
            
            print(f"created pig_farm_id = {pig_farm_id}")
            assert(pig_farm_id > 0)
            
        
        # Test pig_farm duplicate
        url = BASE_URL + 'pig_farm/add'
            
        data = {
            "uhid":         user_uhid,
            "name":         farm_name
        }

        print(f'\n\n*****  Testing duplicate adding pig_farm; url = {url} ; data')
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
            "pig_farm_hid": farm_hid,
            "name":         farm_name + now_ts,
            "adrs_level_1_id": 1,
            "adrs_level_2_id": 2,
            "latitude":     10.262995, 
            "longitude":    123.686722
        }
        
        
        print(f'\n\n*****  Testing farm_update; url = {url} ; data')
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
        
        
    def test_acc_gestating_ops(self, user_id, skip_step = 0):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f'\n\n#################  {now_ts}  #####################################################################')
        
        
        if skip_step & 0x01 == 0: 
        
            url = BASE_URL + 'acc_gestating_ops/add'
            
            data = {
                "uhid":         user_uhid,
                "name":                 SAMPLE_CUSTOMIZED_GESTATING_OPS['name'],
                "num_days_since_insem": SAMPLE_CUSTOMIZED_GESTATING_OPS['num_days_since_insem'],
                "description":          SAMPLE_CUSTOMIZED_GESTATING_OPS['description']
            }
            

            print(f'*****  Testing adding acc_gestating_ops; url = {url} ; data')
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
            
            
            acc_gestating_ops_hid  = res_json['acc_gestating_ops']['hid']
            res_decrypt             = hashids_common.decrypt(acc_gestating_ops_hid)
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
            

        print(f'\n\n***** Testing duplicate adding acc_gestating_ops; url = {url} ; data')
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
            "acc_gest_ops_hid":     acc_gestating_ops_hid,
            "name":                 SAMPLE_CUSTOMIZED_GESTATING_OPS['name'] + now_ts,
            "num_days_since_insem": SAMPLE_CUSTOMIZED_GESTATING_OPS['num_days_since_insem'],
            "description":          SAMPLE_CUSTOMIZED_GESTATING_OPS['description']
        }
        
        
        print(f'\n\n*****  Testing acc_gestating_ops update; url = {url} ; data')
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
        
       
    def test_pig_race_line(self, user_id, account_hid, skip_step = 0):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f'\n\n#################  {now_ts}  #####################################################################')
        
        
        if skip_step & 0x01 == 0: 
        
            url = BASE_URL + 'pig_race_line/add'
            
            data = {
                "uhid":                 user_uhid,
                "pig_race_id":          1,
                "name":                 SAMPLE_PIG_RACE_LINE['name'],
                "description":          SAMPLE_PIG_RACE_LINE['description']
            }
            

            print(f'***** Testing adding pig_race_line; url = {url} ; data')
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
            
            
            is_id_visible = True if 'id' in res_json['pig_race_line'] else False
            assert(is_id_visible == False)
            
            
            pig_race_line_hid  = res_json['pig_race_line']['hid']
            res_decrypt         = hashids_common.decrypt(pig_race_line_hid)
            pig_race_line_id    = res_decrypt[0]
            
            print(f"pig_race_line_id = {pig_race_line_id}")
            assert(pig_race_line_id > 0)
            
        
        # Test pig_race_line add duplicate
        url = BASE_URL + 'pig_race_line/add'
            
        data = {
            "uhid":                 user_uhid,
            "pig_race_id":          1,
            "name":                 SAMPLE_PIG_RACE_LINE['name'],
            "description":          SAMPLE_PIG_RACE_LINE['description']
        }
            

        print(f'\n\n***** Testing duplicate adding pig_race_line; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        
        
        # Test pig_race_line update
        now             = datetime.now()
        now_ts          = now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'pig_race_line/update'
        
        data = {
            "uhid":                 user_uhid,
            "pig_race_line_hid":    pig_race_line_hid,
            "pig_race_id":          1,
            "name":                 SAMPLE_PIG_RACE_LINE['name'] + now_ts,
            "description":          SAMPLE_PIG_RACE_LINE['description']
        }
        
        
        print(f'\n\n***** Testing pig_race_line update; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
        # Add new pig_race_line
        now             = datetime.now()
        now_ts          = now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'pig_race_line/add'
            
        data = {
            "uhid":                 user_uhid,
            "pig_race_id":          1,
            "name":                 SAMPLE_PIG_RACE_LINE['name'] + now_ts,
            "description":          SAMPLE_PIG_RACE_LINE['description']
        }
        

        print(f'\n\n***** Testing adding pig_race_line; url = {url} ; data')
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
        
        
        is_id_visible = True if 'id' in res_json['pig_race_line'] else False
        assert(is_id_visible == False)
        
        new_pig_race_line_hid = res_json['pig_race_line']['hid']
        
        
        # Test delete pig_race_line
        url = BASE_URL + 'pig_race_line/delete?uhid=' + user_uhid + '&pig_race_line_hid=' + new_pig_race_line_hid
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f'\n\n***** Testing pig_race_line delete; url = {url} ')
        print(f"\n\nResult; status_code = {r.status_code}; result")
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
        # Test get_list pig_race_line
        url = BASE_URL + 'pig_race_line/list?ahid=' + account_hid + '&inc_deleted=1&inc_user_audit=1'
        
        print(f'\n\nTesting pig_race_line get_list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        len_items = len(res_json['data'])
        assert(len_items > 0)
        
        return {
            'pig_race_line_id': pig_race_line_id
        }
        
       
    def test_sow_boar_add_multi(self, user_id, pig_farm_id, sex= 'F', num = 3):
        count = 0
        
        
        while count < num:
            s = f"Adding {count+1} of {num} "
            if sex == 'F': 
                s += "sows"
            else:
                s += "boars"
            
            if count == 0:
                self.test_sow_boar_add(user_id, pig_farm_id, sex, opt_msg = s)
            else:
                self.test_sow_boar_add(user_id, pig_farm_id, sex, 
                        skip_flag = 1, opt_msg = s)
                
            count += 1
    
    
    def test_sow_boar_add(self, user_id, pig_farm_id, sex= 'F', skip_flag = 0, 
            opt_msg = None):
        """
        skip_flag:
        bit_0: if > 0, skip update
        """
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f'\n\n#################  {now_ts}  #####################################################################')
        
        
        user_uhid   = hashids_user.encrypt(user_id)
        pfhid       = hashids_common.encrypt(pig_farm_id)
        
        # Get sow list first for pig farm_name
        if sex =='F':
            sow_boar_names = RANDOM_SOW_NAMES
            url = BASE_URL + 'sow_boar/list?pfhid=' + pfhid + '&sex=F&order_by=1' 
        else:
            sow_boar_names = RANDOM_BOAR_NAMES
            url = BASE_URL + 'sow_boar/list?pfhid=' + pfhid + '&sex=M&order_by=1'
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        #print(f"\n\nResult; status_code = {r.status_code}; result")
        #pprint.pprint(res_json)
        
        
        
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
        
        if opt_msg is not None: print(opt_msg)
        print(f'***** Testing adding sow_boar entry; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code} ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
        sow_boar_hid = res_json['sow_boar']['hid']
        
        
        if skip_flag & 0x01 == 0:
        
            # Test sow boar update
            now             = datetime.now()
            now_ts          = now.strftime('%Y%m%d_%H%M%S')
            
            new_name        = sow_boar_name + now_ts
            new_name        = new_name[0:20]
            
            
            url = BASE_URL + 'sow_boar/update'
            
            data = {
                "uhid": user_uhid,
                "sow_boar_hid": sow_boar_hid,
                
                
                "number":   str(sow_boar_number),
                "name":     new_name,
                "notes":    "Updated sow boar"
                
            }
            
            
            print(f'\n\n***** Testing sow_boar_update; url = {url} ; data')
            pprint.pprint(data)
            
            r = requests.post(url, json = data)
            res_text = str(r.text)
            res_json = json.loads(res_text)
            
            print(f"\n\nResult; status_code = {r.status_code}; result = ")
            pprint.pprint(res_json)
            
            result_num  = res_json['result']['num']
            assert(result_num == 0)
            
        
    def test_sow_boar_dispose(self, user_id, pig_farm_id, sex):
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f'\n\n###############################  {now_ts}  ####################################################')
        
        
        user_uhid   = hashids_user.encrypt(user_id)
        pfhid       = hashids_common.encrypt(pig_farm_id)
        
        url = BASE_URL + 'sow_boar/list?pfhid=' + pfhid  + '&sex=' + sex
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        sow_boar_list = res_json['data']
        
        len_items       = len(sow_boar_list)
        assert(len_items > 0)
        
        index           = random.randint(0, len_items-1)
        sow_boar        = sow_boar_list[index]
        sow_boar_hid    = sow_boar['hid'] 
        
            
        dispose_status_ids = [5,6,7,8]
        len_items   = len(dispose_status_ids)
        index       = random.randint(0, len_items-1)
        dispose_status_id    = dispose_status_ids[index]
        
        
        now             = datetime.now()
        now_dt_s        = now.strftime('%Y-%m-%d')
        now_ts          = now.strftime('%Y%m%d_%H%M%S')
        
        
        url = BASE_URL + 'sow_boar/dispose'
            
        data = {
            "uhid":             user_uhid,
            "sow_boar_hid":     sow_boar_hid,
            
            "dispose_status_id":dispose_status_id,
            "date_dispose":     now_dt_s,
            "dispose_notes":    "disposed sow boar " + now_ts
            
        }
        
        print(f'\n\n***** Testing sow_boar_dispose; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
    def test_semen_source(self, user_id, pig_farm_id):
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f'\n\n###############################  {now_ts}  ####################################################')
        
        
        user_uhid   = hashids_user.encrypt(user_id)
        pfhid       = hashids_common.encrypt(pig_farm_id)
        
        # Get boar list of the farm
        
        url = BASE_URL + 'sow_boar/list?pfhid=' + pfhid + '&sex=M'
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        boar_id     = 0
        boar_list   = res_json['data']
        len_boar    = len(boar_list)
        
        if len_boar > 1:
            index_boar  = random.randint(0, len_boar-1)
            cur_boar    = boar_list[index_boar]
            
        else:
            cur_boar    = boar_list[0]
            
        boar_name   = cur_boar['name']
        boar_hid    = cur_boar['hid']
    
       
        # add semen_source by boar_hid 
        
        url = BASE_URL + 'semen_source/add'
       
        
        data = {
          "uhid": user_uhid,
          "pfhid": pfhid,
          
          "boar_hid": boar_hid,
          "name":   'Semen from Butakal - ' + boar_name
        }
        
        print(f'\n\nTesting adding semen_source entry; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code} ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
        
        # add semen_source by external semen_supplier id
        
        url = BASE_URL + 'semen_supplier/list?inc_deleted=0&inc_user_audit=0'
        
        print(f'\n\n****** Testing semen_supplier get_list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        
        semen_supplier_list = res_json['data']
        len_items = len(semen_supplier_list)
        assert(len_items > 0)
        
        
        if len_items == 1:
            index = 0
        else:
            index = random.randint(0, len_items - 1)
        
        semen_supplier = semen_supplier_list[index] 
        
        semen_supplier_hid = semen_supplier['hid']
        
        
        url = BASE_URL + 'semen_source/add'
       
        
        data = {
          "uhid": user_uhid,
          "pfhid": pfhid,
          "semen_supplier_hid": semen_supplier_hid,
          "pig_race_line_hid": 'Q92W83',
              
          "name":   'PIC 337'
        }
        
        
        print(f'\n\nTesting adding semen_source entry; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code} ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
    def test_auto_clean_data(self, user_id, acc_name, farm_name):
        res_register = self.test_account_register(user_id, acc_name)
        account_id  = res_register['account_id']
        account_hid  = res_register['account_hid']
       
        res_pig_farm = self.test_pig_farm(user_id, farm_name)
        
        pig_farm_id = res_pig_farm['pig_farm_id']
        self.test_sow_boar_add_multi(user_id, pig_farm_id, sex= 'F', num = 10)
        self.test_sow_boar_add_multi(user_id, pig_farm_id, sex= 'M', num = 3)
        
        self.test_sow_boar_dispose(user_id, pig_farm_id, 'F')
        self.test_sow_boar_dispose(user_id, pig_farm_id, 'F')
        
        self.test_semen_source(user_id, pig_farm_id)
        
        
        
if __name__ == '__main__':
    t = TestAPIAccount()
    
    t.test_auto_clean_data(1, "Jackson Farm", "Punod Farm")