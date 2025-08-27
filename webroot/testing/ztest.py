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
'Linda', 'Kikay', 'Diday', 'Puring', 'Bentay', 'Indang'

]

RANDOM_BOAR_NAMES = ['Berto', 'Kurdapyo', 'KiKoY', 'Didoy', 'Gorio', 'Desidido',
'Ondo', 'Juaning', 'Kokoy', 'Dodo', 'Nanding', 'Bitoy'
]


RANDOM_STAFF_NAMES = ['Arnel', 'Kevin', 'Michael', 'Hilmero', 'Bogart']


SAMPLE_CUSTOMIZED_GESTATING_OPS = {
    "name":         "Inject Vitamins",
    "description":  "Inject vitamin Z",
    "num_days_since_insem": 50    
}

SAMPLE_PIG_RACE_LINE = {
    "name":         "Camborough 48",
    "description":  "PIC camborough 48"
}



class TestAPIAccount:
    def __init__(self):
        self.summary    = {
            'account':          {},
            'account_request':  {},
            'user_group':       {},
            
            'pig_farm':         {},
            'pig_farm_staff':   {},
            'pig_race':         {},
            'pig_race_line':    {},
            
            'acc_gestating_ops':{},
            'acc_lactating_ops':{},
   
            'semen_supplier':   {},
            'feed_supplier':    {},
            'feed_brand':       {},
            'feed_type':        {},
            
            'sow_boar':         {},
            'semen_source':     {},
   
            'pig_production':   {}
        }
    
    
    def test_account_register(self, user_id, acc_name, skip_step = 0):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {now_ts}  ###########################")
        
        
        if skip_step & 0x01 == 0: 
            url = BASE_URL + 'account/register'
            
            data = {
                "uhid":         user_uhid,
                "name":         acc_name,
                "country_id":   1
            }
            
            
            print(f"***** Testing adding account_register; url = {url} ; data")
            pprint.pprint(data)
            
            r = requests.post(url, json = data)
            res_text = str(r.text)
            res_json = json.loads(res_text)
        
            print(f"\n\nResult; status_code = {r.status_code}; result =")
            pprint.pprint(res_json)
            
            result_num  = res_json['result']['num']
            assert(result_num == 0)
            
            self.summary['account']['register'] = 'OK'
            
            
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

        print(f"\n\n*****  Testing duplicate account_register; url = {url} ; data")
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        assert(res_json['result']['code'] == 'RES_NUM_ACCOUNT_ALREADY_REGISTERED_FOR_USER')
        
        self.summary['account']['register_duplicate_check'] = 'OK'
        
        
        # Test account update
        now             = datetime.now()
        now_ts          = now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'account/update'
        
        data = {
            "uhid":         user_uhid,
            "name":         acc_name + now_ts
        }
        
        
        print(f"\n\n***** Testing account_update; url = {url} ; data")
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        self.summary['account']['update'] = 'OK'
        
        
        print(f"\n\n***** Testing get account user groups; account_id = {account_id}")
        url = BASE_URL + 'user_group/list?ahid=' + account_hid
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        len_items = len(res_json['data'])
        assert(len_items == 3)
        
        self.summary['account']['user_groups_list'] = 'OK'
        
        
        self.test_acc_gestating_ops(user_id)
        
        print(f'\n\n***** Testing get account gestating_ops; account_id = {account_id}')
        res = model['acc_gestating_ops'].get_list(account_id)
        
        print(f'\n\nAccount gestating_ops; len = {len(res)}')
        pprint.pprint(res)
        assert(len(res) >= 3)
        
        self.summary['account']['gestating_ops_list'] = 'OK'
        
        
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
        print(f"\n\n#################  {now_ts}  ###########################")
        
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

        self.summary['semen_supplier']['add'] = 'OK'
        
    
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
        
        self.summary['semen_supplier']['list'] = 'OK'
        
        
    
    def test_feed_brand(self, user_id):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {now_ts}  ###########################")
        
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

        self.summary['feed_brand'] = {}
        self.summary['feed_brand']['add'] = 'OK'
        
        
        
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

        self.summary['feed_brand']['add'] = 'OK'
        
        
        
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
        
        
        self.summary['feed_brand']['list'] = 'OK'
    
    
    def test_feed_supplier(self, user_id):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {now_ts}  ###########################")
        
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


        self.summary['feed_supplier']['add'] = 'OK'
        
    
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
        
        self.summary['feed_supplier']['list'] = 'OK'
    
        
    def test_pig_farm(self, user_id, farm_name, skip_step = 0):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {now_ts}  ###########################")
        
        
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


            self.summary['pig_farm']['add'] = 'OK'
            
            
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
 
        assert(res_json['result']['code'] == 'RES_NUM_DUPLICATE_ENTRY')
        
        self.summary['pig_farm']['add_duplicate_check'] = 'OK'
        
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
        
        self.summary['pig_farm']['update'] = 'OK'
        
        return {
            'pig_farm_id': pig_farm_id
        }
        
        
    def test_pig_farm_staff(self, user_id, pig_farm_id, skip_step = 0):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {now_ts}  ###########################")
        
        pig_farm_hid    = hashids_common.encrypt(pig_farm_id)
        
        if skip_step & 0x01 == 0: 
            
            len_items       = len(RANDOM_STAFF_NAMES)
            
            index           = random.randint(0, len_items-1)
            staff_name      = RANDOM_STAFF_NAMES[index]
            
        
            url = BASE_URL + 'pig_farm_staff/add'
            
            data = {
                "uhid":                 user_uhid,
                "pig_farm_hid":         pig_farm_hid,
                "name":                 staff_name
            }
            

            print(f"***** Testing adding pig_farm_staff; url = {url} ; data")
            pprint.pprint(data)
            
            r = requests.post(url, json = data)
            res_text = str(r.text)
            res_json = json.loads(res_text)
            
            print(f"\n\nResult; status_code = {r.status_code}; result")
            pprint.pprint(res_json)
            
            result_num  = res_json['result']['num']
            assert(result_num == 0)


            self.summary['pig_farm_staff']['add'] = 'OK'
            
            
            is_id_visible = True if 'id' in res_json['pig_farm_staff'] else False
            assert(is_id_visible == False)
            
            
            pig_farm_staff_hid  = res_json['pig_farm_staff']['hid']
            res_decrypt         = hashids_common.decrypt(pig_farm_staff_hid)
            pig_farm_staff_id    = res_decrypt[0]
            
            print(f"pig_farm_staff_id = {pig_farm_staff_id}")
            assert(pig_farm_staff_id > 0)
            
        
        # Test pig_farm_staff add duplicate
        url = BASE_URL + 'pig_farm_staff/add'
            
        data = {
            "uhid":                 user_uhid,
            "pig_farm_hid":         pig_farm_hid,
            "name":                 staff_name
        }

        print(f'\n\n***** Testing duplicate adding pig_farm_staff; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        assert(res_json['result']['code'] == 'RES_NUM_DUPLICATE_ENTRY')
        
        self.summary['pig_farm_staff']['add_duplicate_check'] = 'OK'
            
        
        
        # Test pig_farm_staff update
        now             = datetime.now()
        now_ts          = now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'pig_farm_staff/update'
        
        data = {
            "uhid":                 user_uhid,
            "pig_farm_hid":         pig_farm_hid,
            "pig_farm_staff_hid":   pig_farm_staff_hid,
            "name":                 staff_name + now_ts
        }
        
        
        print(f'\n\n***** Testing pig_farm_staff update; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        self.summary['pig_farm_staff']['update'] = 'OK'
        
        
        # Add new pig_farm_staff
        now             = datetime.now()
        now_ts          = now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'pig_farm_staff/add'
            
        data = {
            "uhid":                 user_uhid,
            "pig_farm_hid":         pig_farm_hid,
            "name":                 staff_name + now_ts
        }
        

        print(f'\n\n***** Testing adding pig_farm_staff; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)

       
        
        is_id_visible = True if 'id' in res_json['pig_farm_staff'] else False
        assert(is_id_visible == False)
        
        new_pig_farm_staff_hid = res_json['pig_farm_staff']['hid']
        
        
        # Test delete pig_farm_staff
        url = BASE_URL + 'pig_farm_staff/delete?uhid=' + user_uhid + '&pig_farm_staff_hid=' + new_pig_farm_staff_hid
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f'\n\n***** Testing pig_farm_staff delete; url = {url} ')
        print(f"\n\nResult; status_code = {r.status_code}; result")
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        self.summary['pig_farm_staff']['delete'] = 'OK'
        
        
        
        # Test get_list pig_farm_staff
        url = BASE_URL + 'pig_farm_staff/list?pfhid=' + pig_farm_hid + '&inc_deleted=1&inc_user_audit=1'
        
        print(f'\n\nTesting pig_farm_staff get_list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        len_items = len(res_json['data'])
        assert(len_items > 0)
        
        self.summary['pig_farm_staff']['list'] = 'OK'
        
        return {
            'pig_farm_staff_id': pig_farm_staff_id
        }
    
        
    def test_acc_gestating_ops(self, user_id, skip_step = 0):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {now_ts}  ###########################")
        
        
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

            self.summary['acc_gestating_ops']['add'] = 'OK'
            
            
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
 
        assert(res_json['result']['code'] == 'RES_NUM_DUPLICATE_ENTRY')
        
        self.summary['acc_gestating_ops']['add_duplicate_check'] = 'OK'
            
        
        
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
        
        self.summary['acc_gestating_ops']['update'] = 'OK'
        
        
        return {
            'acc_gestating_ops_id': acc_gestating_ops_id
        }
        
       
    def test_pig_race_line(self, user_id, account_hid, skip_step = 0):
        user_uhid   = hashids_user.encrypt(user_id)
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {now_ts}  ###########################")
        
        
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

            self.summary['pig_race_line']['add'] = 'OK'
            
            
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
 
        assert(res_json['result']['code'] == 'RES_NUM_DUPLICATE_ENTRY')
        
        self.summary['pig_race_line']['add_duplicate_check'] = 'OK'
            
        
        
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
        
        self.summary['pig_race_line']['update'] = 'OK'
        
        
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
        
        self.summary['pig_race_line']['delete'] = 'OK'
        
        
        
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
        
        self.summary['pig_race_line']['list'] = 'OK'
        
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
        print(f"\n\n#################  {now_ts}  ###########################")
        
        
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
        
        self.summary['sow_boar']['list'] = 'OK'
        
        
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
        
        self.summary['sow_boar']['add'] = 'OK'
        
        
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
            
            self.summary['sow_boar']['update'] = 'OK'
            
            
        
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
        
        self.summary['sow_boar']['dispose'] = 'OK'
        
        
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
       
        
        data_semen_source_1 = {
          "uhid": user_uhid,
          "pfhid": pfhid,
          
          "boar_hid": boar_hid,
          "name":   'Semen from Butakal - ' + boar_name
        }
        data = data_semen_source_1
        
        print(f'\n\nTesting adding semen_source entry; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code} ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
        self.summary['semen_source']['by_boar'] = {}
        self.summary['semen_source']['by_boar']['add'] = 'OK'
        
        
        semen_source_hid_1 = res_json['semen_source']['hid']
        
        
        # Test semen_source add duplicate
        url = BASE_URL + 'semen_source/add'
            
        data = data_semen_source_1

        print(f'\n\n***** Testing duplicate adding semen_source; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        assert(res_json['result']['code'] == 'RES_NUM_DUPLICATE_ENTRY')
        
        self.summary['semen_source']['by_boar']['add_duplicate_check'] = 'OK'
        
        
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
       
        
        data_semen_source_2 = {
          "uhid": user_uhid,
          "pfhid": pfhid,
          "semen_supplier_hid": semen_supplier_hid,
          "pig_race_line_hid": 'Q92W83',
              
          "name":   'PIC 337'
        }
        data = data_semen_source_2
        
        print(f'\n\nTesting adding semen_source entry; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code} ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
        self.summary['semen_source']['by_semen_supplier'] = {}
        self.summary['semen_source']['by_semen_supplier']['add'] = 'OK'
        
        
        # Test semen_source add duplicate
        url = BASE_URL + 'semen_source/add'
            
        data = data_semen_source_2

        print(f'\n\n***** Testing duplicate adding semen_source; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        assert(res_json['result']['code'] == 'RES_NUM_DUPLICATE_ENTRY')
        
        self.summary['semen_source']['by_semen_supplier']['add_duplicate_check'] = 'OK'
        
        
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
        
        self.test_pig_farm_staff(user_id, pig_farm_id)
        
        self.test_semen_source(user_id, pig_farm_id)
        
        print('\n\nTest Summary')
        pprint.pprint(self.summary)
        
  
        
if __name__ == '__main__':
    t = TestAPIAccount()
    
    t.test_auto_clean_data(1, "Jackson Farm", "Punod Farm")