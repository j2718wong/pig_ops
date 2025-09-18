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
import copy
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


RANDOM_SOW_NAMES_1 = [
'Soling', 'Sita', 'Kurdapya', 'Imyat', 'Tasing', 'Narsing', 'Medi', 
'Segunda', 'Berta', 'Osang', 'Petra',  'Nitang',  'Menang', 'Adela',
'Linda', 'Kikay', 'Diday', 'Puring', 'Bentay', 'Indang'
]

RANDOM_SOW_NAMES_2 = [
'Landa', 'Ging2x', 'Agnes', 'Conching'
]



RANDOM_BOAR_NAMES = ['Berto', 'Kurdapyo', 'KiKoY', 'Didoy', 'Gorio', 'Desidido',
'Ondo', 'Juaning', 'Kokoy', 'Dodo', 'Nanding', 'Bitoy'
]


RANDOM_STAFF_NAMES = ['Arnel', 'Kevin', 'Michael', 'Hilmero', 'Bogart', 'Ruben']


SAMPLE_CUSTOMIZED_GESTATING_OPS = {
    "name":         "Inject Vitamin Z",
    "description":  "Inject vitamin Z",
    "num_days_since": 50    
}


SAMPLE_CUSTOMIZED_LACTATING_OPS = {
    "name":         "Inject Vitamin Q",
    "description":  "Inject vitamin Q",
    "num_days_since": 24
}


SAMPLE_PIG_RACE_LINE = {
    "name":         "Camborough 48",
    "description":  "PIC camborough 48"
}


ADRS_LEVEL_1_ID_CEBU_PROV    = 49

ADRS_LEVEL_2_ID_ARGAO        = 987
ADRS_LEVEL_2_ID_TALISAY      = 1029
ADRS_LEVEL_2_ID_MINGLA       = 1011
ADRS_LEVEL_2_ID_NAGA         = 1013

ADRS_LEVEL_3_ID_BALIRONG     = 27013
ADRS_LEVEL_3_ID_TAGJAGUIMIT  = 27033
ADRS_LEVEL_3_ID_TABUNOC      = 27323


RANDOM_PIG_BUYERS = [

{
    'name': 'Segundo Facundo Impacto',
    'address_level_1_id':  ADRS_LEVEL_1_ID_CEBU_PROV,
    'address_level_2_id':  ADRS_LEVEL_2_ID_NAGA,
    'address_level_3_id':  ADRS_LEVEL_3_ID_BALIRONG,
    'contact_number':   '09178888567',
    'whatsapp':         '0987567898',
    'messenger':    'Segundo Facundo'
},

{
    'name': 'Desidido Muhabal Jr',
    'address_level_1_id':  ADRS_LEVEL_1_ID_CEBU_PROV,
    'address_level_2_id':  ADRS_LEVEL_2_ID_MINGLA,
    'contact_number':   '0917123456',
    'whatsapp':         '0987567000',
    'messenger':    'Desidido Muhabal'
},


{
    'name': 'Epitacia U Cabrera',
    'address_level_1_id':  ADRS_LEVEL_1_ID_CEBU_PROV,
    'address_level_2_id':  ADRS_LEVEL_2_ID_TALISAY,
    'address_level_3_id':  ADRS_LEVEL_3_ID_TABUNOC,
    'contact_number':   '091710986',
    'whatsapp':         '087969000',
    'messenger':    'Epitacia Cabrera'
}


]




PIG_OPERATION_TYPE_GESTATING        = 1
PIG_OPERATION_TYPE_LACTATING_PIGLETS        = 2
PIG_OPERATION_TYPE_GROWING          = 3

class TestBase:
    def __init__(self, business_object, summary):
        self.business_object    = business_object
        
        self.summary            = summary
        
    
    def test_duplicate_check(self, url, data):
        values = (self.business_object, url)
        s = '\n\n***** Testing duplicate adding %s; url = %s; data' %values
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        assert(res_json['result']['code'] == 'RES_NUM_DUPLICATE_ENTRY')
        
        self.summary[self.business_object]['add_duplicate_check'] = 'OK'



class TestFeedSupplier(TestBase):
    def __init__(self, summary):
        self.business_object = 'feed_supplier'
        super().__init__(self.business_object, summary)
        
        self.url_add    = BASE_URL + 'feed_supplier/add'
        
    
    def test_add(self, user_id):
        user_uhid   = hashids_user.encrypt(user_id)
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
            
        data = {
            "uhid":         user_uhid,
            "name":         'Ayan Sampan',
            "address_level_1_id":   ADRS_LEVEL_1_ID_CEBU_PROV,
            "address_level_2_id":   ADRS_LEVEL_2_ID_NAGA,
            "address_level_3_id":   ADRS_LEVEL_3_ID_TAGJAGUIMIT
        }
        

        print(f'***** Testing add {self.business_object}; url = {self.url_add} ; data')
        pprint.pprint(data)
        
        r = requests.post(self.url_add, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
        feed_supplier_hid = res_json['feed_supplier']['hid']
        data['feed_supplier_hid'] = feed_supplier_hid

        self.summary['feed_supplier']['add'] = 'OK'
        
        return data
        
        
    def test_update(self, data):
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'feed_supplier/update'
        
        data['name']    = data['name'] + dt_now_s
              
        
        print(f'\n\n*****  Testing update {self.business_object}; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        self.summary['feed_supplier']['update'] = 'OK'
        
        
    def test_get_list(self, address_level_2_id):
        # Test get_list feed_supplier
        url = BASE_URL + 'feed_supplier/list?address_level_2_id=%s' % address_level_2_id
        
        print(f'\n\n****** Testing feed_suppler get_list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
    
        len_items = len(res_json['data'])
        assert(len_items > 0)
        
        self.summary['feed_supplier']['list'] = 'OK'
    

class TestSemenSupplier(TestBase):
    def __init__(self, summary):
        self.business_object = 'semen_supplier'
        super().__init__(self.business_object, summary)
        
        self.url_add    = BASE_URL + 'semen_supplier/add'
        
    
    def test_add(self, user_id):
        user_uhid   = hashids_user.encrypt(user_id)
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
        url = BASE_URL + 'semen_supplier/add'
            
        data = {
            "uhid":         user_uhid,
            "name":                 'Growbest Agrivet',
            "address_level_1_id":   ADRS_LEVEL_1_ID_CEBU_PROV,
            "address_level_2_id":   ADRS_LEVEL_2_ID_ARGAO
        }
        

        print(f'***** Testing add {self.business_object}; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)

        semen_supplier_hid = res_json['semen_supplier']['hid']
        data['semen_supplier_hid'] = semen_supplier_hid

        self.summary[self.business_object]['add'] = 'OK'
        
        return data
        
    
    def test_get_list(self):
        # Test get_list semen_supplier
        url = BASE_URL + 'semen_supplier/list'
        
        print(f'\n\n****** Testing semen_supplier get_list; url = {url} address_level_2_id=1')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        len_items = len(res_json['data'])
        assert(len_items > 0)
        
        self.summary['semen_supplier']['list'] = 'OK'
    
    

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
            
            'account_pig_ops':  {},
   
            'semen_supplier':   {},
            'feed_supplier':    {},
            'feed_brand':       {},
            'feed_type':        {},
            
            'sow_boar':         {},
            'semen_source':     {},
   
            'pig_production':   {}
        }
    
    
    def test_account_register(self, user_id, acc_name):
        user_uhid   = hashids_user.encrypt(user_id)
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
        
        
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
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'account/update'
        
        data = {
            "uhid":         user_uhid,
            "name":         acc_name + dt_now_s
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
        
        
        self.test_account_pig_ops(user_id, PIG_OPERATION_TYPE_GESTATING)
        
        print(f'\n\n***** Testing get account_pig_ops list; account_id = {account_id}')
        res = model['account_pig_ops'].get_list(account_id, PIG_OPERATION_TYPE_GESTATING)
        len_items = len(res)
        
        print(f'\n\nAccount gestating_ops; len = {len_items}')
        pprint.pprint(res)
        assert(len_items>= 3)
        
        self.summary['account']['gestating_ops_list'] = 'OK'
        
        
        self.test_account_pig_ops(user_id, PIG_OPERATION_TYPE_LACTATING_PIGLETS)
        
        print(f'\n\n***** Testing get account_pig_ops; account_id = {account_id}')
        res = model['account_pig_ops'].get_list(account_id, PIG_OPERATION_TYPE_LACTATING_PIGLETS)
        len_items = len(res)
        
        print(f'\n\nAccount lactating_ops; len = {len_items}')
        pprint.pprint(res)
        assert(len_items >= 4)
        
        self.summary['account']['lactating_ops_list'] = 'OK'
        
        
        self.test_pig_race_line(user_id, account_hid)
        
        self.test_semen_supplier(user_id)
        
        self.test_feed_brand(user_id)
        self.test_feed_supplier(user_id)
        
        
        
        
        
        return {
            'account_id':       account_id,
            'account_hid':     account_hid,
        }
        
    
    def test_semen_supplier(self, user_id):
        t = TestSemenSupplier(self.summary)
        data_input = t.test_add(user_id)
        
        t.test_duplicate_check(t.url_add, data_input)
        
        #t.test_update(data_input)
        

    def test_feed_brand(self, user_id):
        user_uhid   = hashids_user.encrypt(user_id)
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
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
        t = TestFeedSupplier(self.summary)
        data_input = t.test_add(user_id)
        
        t.test_duplicate_check(t.url_add, data_input)
        
        t.test_update(data_input)
        
        address_level_2_id = ADRS_LEVEL_2_ID_NAGA
        t.test_get_list(address_level_2_id)
    
        
    def test_pig_farm(self, user_id, farm_name):
        user_uhid   = hashids_user.encrypt(user_id)
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
        
        url = BASE_URL + 'pig_farm/add'
        
        data = {
            "uhid":             user_uhid,
            "name":             farm_name,
            "address_level_1_id":  ADRS_LEVEL_1_ID_CEBU_PROV,
            "address_level_2_id":  ADRS_LEVEL_2_ID_NAGA,
            "address_level_3_id":  ADRS_LEVEL_3_ID_TAGJAGUIMIT
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
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'pig_farm/update'
        
        data = {
            "uhid":         user_uhid,
            "pig_farm_hid": farm_hid,
            "name":         farm_name + dt_now_s,
            "address_level_1_id": 1,
            "address_level_2_id": 2,
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
        
        
    def test_pig_farm_staff(self, user_id, pig_farm_id, num_staff = 3):
        user_uhid   = hashids_user.encrypt(user_id)
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
        pig_farm_hid    = hashids_common.encrypt(pig_farm_id)
        
           
        len_items       = len(RANDOM_STAFF_NAMES)
        
        count = 0
        
        while count < num_staff:
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
            
            count += 1
        
        
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
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'pig_farm_staff/update'
        
        data = {
            "uhid":                 user_uhid,
            "pig_farm_hid":         pig_farm_hid,
            "pig_farm_staff_hid":   pig_farm_staff_hid,
            "name":                 staff_name + dt_now_s
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
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'pig_farm_staff/add'
            
        data = {
            "uhid":                 user_uhid,
            "pig_farm_hid":         pig_farm_hid,
            "name":                 staff_name + dt_now_s
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
    
        
    def test_account_pig_ops(self, user_id, operation_type):
        user_uhid       = hashids_user.encrypt(user_id)
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
        
        url = BASE_URL + 'account_pig_ops/add'
        
        if operation_type == PIG_OPERATION_TYPE_GESTATING:
            data = {
                "uhid":             user_uhid,
                "operation_type":   operation_type,
                "name":             SAMPLE_CUSTOMIZED_GESTATING_OPS['name'],
                "num_days_since":   SAMPLE_CUSTOMIZED_GESTATING_OPS['num_days_since'],
                "description":      SAMPLE_CUSTOMIZED_GESTATING_OPS['description']
            }
        
        if operation_type == PIG_OPERATION_TYPE_LACTATING_PIGLETS:
            data = {
                "uhid":             user_uhid,
                "operation_type":   operation_type,
                "name":             SAMPLE_CUSTOMIZED_LACTATING_OPS['name'],
                "num_days_since":   SAMPLE_CUSTOMIZED_LACTATING_OPS['num_days_since'],
                "description":      SAMPLE_CUSTOMIZED_LACTATING_OPS['description']
            }
        
        
        s_type = ''
        
        if operation_type == PIG_OPERATION_TYPE_GESTATING:
            s_type = 'PIG_OPERATION_TYPE_GESTATING'
            
        elif operation_type == PIG_OPERATION_TYPE_LACTATING_PIGLETS:
            s_type = 'PIG_OPERATION_TYPE_LACTATING_PIGLETS'
            
        else:
            s_type = 'PIG_OPERATION_TYPE_GROWING'


        print(f'*****  Testing adding account_pig_ops; operation_type ={s_type}; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)

        self.summary['account_pig_ops']['add'] = 'OK'
        
        
        
        account_pig_ops_hid     = res_json['account_pig_ops']['hid']
        res_decrypt             = hashids_common.decrypt(account_pig_ops_hid)
        account_pig_ops_id      = res_decrypt[0]
        
        print(f"account_pig_ops_id = {account_pig_ops_id}")
        assert(account_pig_ops_id > 0)
        
        
        
        # Test account_pig_ops add duplicate
        url = BASE_URL + 'account_pig_ops/add'
        
        print(f'\n\n***** Testing duplicate adding account_pig_ops; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        assert(res_json['result']['code'] == 'RES_NUM_DUPLICATE_ENTRY')
        
        self.summary['account_pig_ops']['add_duplicate_check'] = 'OK'
            

        
        # Test account_pig_ops update
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'account_pig_ops/update'
        
        if operation_type == PIG_OPERATION_TYPE_GESTATING:
            data = {
                "uhid":                     user_uhid,
                "account_pig_ops_hid":      account_pig_ops_hid,
                "operation_type":           operation_type,
                "name":                     SAMPLE_CUSTOMIZED_GESTATING_OPS['name'] + dt_now_s,
                "num_days_since":           SAMPLE_CUSTOMIZED_GESTATING_OPS['num_days_since'],
                "description":              SAMPLE_CUSTOMIZED_GESTATING_OPS['description']
            }
        
        
        if operation_type == PIG_OPERATION_TYPE_LACTATING_PIGLETS:
            data = {
                "uhid":                     user_uhid,
                "account_pig_ops_hid":      account_pig_ops_hid,
                "operation_type":           operation_type,
                "name":                     SAMPLE_CUSTOMIZED_LACTATING_OPS['name'] + dt_now_s,
                "num_days_since":           SAMPLE_CUSTOMIZED_LACTATING_OPS['num_days_since'],
                "description":              SAMPLE_CUSTOMIZED_LACTATING_OPS['description']
            }
        
        
        print(f'\n\n*****  Testing account_pig_ops update; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        self.summary['account_pig_ops']['update'] = 'OK'
        
        
        # Test delete account_pig_ops
        url = BASE_URL + 'account_pig_ops/delete?uhid=' + user_uhid + '&account_pig_ops_hid=' + account_pig_ops_hid
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\n***** Testing account_pig_ops delete; url = {url} ")
        print(f"\n\nResult; status_code = {r.status_code}; result")
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        self.summary['account_pig_ops']['delete'] = 'OK'
        
        
    def test_account_pig_buyer(self, user_id):
        user_uhid       = hashids_user.encrypt(user_id)
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
        
        url = BASE_URL + 'account_pig_buyer/add'
        
        index = 0
        data_to_update = None
        data_to_delete = None
        
        for cur_entry in RANDOM_PIG_BUYERS:
            data = copy.copy(cur_entry)
            data['uhid'] = user_uhid
            
            
            print(f'\n\n*****  Testing account_pig_ops add; url = {url} ; data')
            pprint.pprint(data)
            
            r = requests.post(url, json = data)
            res_text = str(r.text)
            res_json = json.loads(res_text)
            

            print(f"\n\nResult; status_code = {r.status_code}; result = ")
            pprint.pprint(res_json)
            
            result_num  = res_json['result']['num']
            assert(result_num == 0)
            
            account_pig_buyer_hid  = res_json['accout_pig_buyer']['hid'] 
            
            data['account_pig_buyer_hid'] = account_pig_buyer_hid
            
            if index == 1:
                data_to_update = data
            
            if index == 2:
                data_to_delete = data
            
            index += 1
        
        
        
    def test_pig_race_line(self, user_id, account_hid):
        user_uhid   = hashids_user.encrypt(user_id)
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
        

        url = BASE_URL + 'pig_race_line/add'
        
        data = {
            "uhid":                 user_uhid,
            "pig_race_id":          1,
            "name":                 SAMPLE_PIG_RACE_LINE['name'],
            "description":          SAMPLE_PIG_RACE_LINE['description']
        }
        

        print(f"***** Testing adding pig_race_line; url = {url} ; data")
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
            

        print(f"\n\n***** Testing duplicate adding pig_race_line; url = {url} ; data")
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        assert(res_json['result']['code'] == 'RES_NUM_DUPLICATE_ENTRY')
        
        self.summary['pig_race_line']['add_duplicate_check'] = 'OK'
            
        
        
        # Test pig_race_line update
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'pig_race_line/update'
        
        data = {
            "uhid":                 user_uhid,
            "pig_race_line_hid":    pig_race_line_hid,
            "pig_race_id":          1,
            "name":                 SAMPLE_PIG_RACE_LINE['name'] + dt_now_s,
            "description":          SAMPLE_PIG_RACE_LINE['description']
        }
        
        
        print(f"\n\n***** Testing pig_race_line update; url = {url} ; data")
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
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        url = BASE_URL + 'pig_race_line/add'
            
        data = {
            "uhid":                 user_uhid,
            "pig_race_id":          1,
            "name":                 SAMPLE_PIG_RACE_LINE['name'] + dt_now_s,
            "description":          SAMPLE_PIG_RACE_LINE['description']
        }
        

        print(f"\n\n***** Testing adding pig_race_line; url = {url} ; data")
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
        
        print(f"\n\n***** Testing pig_race_line delete; url = {url} ")
        print(f"\n\nResult; status_code = {r.status_code}; result")
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        self.summary['pig_race_line']['delete'] = 'OK'
        
        
        
        # Test get_list pig_race_line
        url = BASE_URL + 'pig_race_line/list?ahid=' + account_hid + '&inc_deleted=1&inc_user_audit=1'
        
        print(f"\n\nTesting pig_race_line get_list; url = {url} ")
        
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
    
    
    def test_sow_boar_add(self, user_id, pig_farm_id, sex= 'F', is_external = 0,
            skip_flag = 0, 
            opt_msg = None):
        """
        skip_flag:
        bit_0: if > 0, skip update
        """
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
        
        user_uhid   = hashids_user.encrypt(user_id)
        pfhid       = hashids_common.encrypt(pig_farm_id)
        
        # Get sow list first for pig farm_name
        if sex =='F':
            sow_boar_names = RANDOM_SOW_NAMES_1
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
                    
        
        dt_now      = datetime.now()
        
        random_num_days = random.randint(0, 60)
        dt_dob      = dt_now - timedelta(days = (210 + random_num_days))
        dt_dob_s    = dt_dob.strftime('%Y-%m-%d')
        
        data = {
          "uhid": user_uhid,
          "pfhid": pfhid,
          
          "sow_status_id": 2,
          "sex": sex,
          "is_external": is_external,
          "number": str(sow_boar_number),
          "name": sow_boar_name,
          "date_of_birth": dt_dob_s
        }
        
        if is_external > 0:
            data['number'] =  None
        
        
        url = BASE_URL + 'sow_boar/add'
        
        if opt_msg is not None: print(opt_msg)
        print(f"***** Testing adding sow_boar entry; url = {url} ; data")
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
            dt_now          = datetime.now()
            dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
            
            new_name        = sow_boar_name + dt_now_s
            new_name        = new_name[0:20]
            
            
            url = BASE_URL + 'sow_boar/update'
            
            data = {
                "uhid": user_uhid,
                "sow_boar_hid": sow_boar_hid,
                
                
                "number":   str(sow_boar_number),
                "name":     new_name,
                "notes":    "Updated sow boar"
                
            }
            
            
            print(f"\n\n***** Testing sow_boar_update; url = {url} ; data")
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
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n###############################  {dt_now_s}  ####################################################")
        
        
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
        
        
        dt_now          = datetime.now()
        now_dt_s        = dt_now.strftime('%Y-%m-%d')
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        
        url = BASE_URL + 'sow_boar/dispose'
            
        data = {
            "uhid":             user_uhid,
            "sow_boar_hid":     sow_boar_hid,
            
            "dispose_status_id":dispose_status_id,
            "date_dispose":     now_dt_s,
            "dispose_notes":    "disposed sow boar " + dt_now_s
            
        }
        
        print(f"\n\n***** Testing sow_boar_dispose; url = {url} ; data")
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
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n###############################  {dt_now_s}  ####################################################")
        
        
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
        
        print(f"\n\n****** Testing semen_supplier get_list; url = {url} ")
        
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
        
        print(f"\n\nTesting adding semen_source entry; url = {url} ; data")
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
        
        s =  '\n\n\nTesting on '
        
        if USING_PRODUCTION_DB > 0:
            s += ' PRODUCTION database'
        else:
            s += ' DEV database'
        s += '\n\n'
            
        print(s)
        
        res_register = self.test_account_register(user_id, acc_name)
        account_id  = res_register['account_id']
        account_hid  = res_register['account_hid']
       
        res_pig_farm = self.test_pig_farm(user_id, farm_name)
        
        pig_farm_id = res_pig_farm['pig_farm_id']
        self.test_sow_boar_add_multi(user_id, pig_farm_id, sex= 'F', num = 10)
        self.test_sow_boar_add_multi(user_id, pig_farm_id, sex= 'M', num = 3)
        
        self.test_sow_boar_add(user_id, pig_farm_id, sex= 'M', is_external = 1)
        
        self.test_sow_boar_dispose(user_id, pig_farm_id, 'F')
        self.test_sow_boar_dispose(user_id, pig_farm_id, 'F')
        
        self.test_pig_farm_staff(user_id, pig_farm_id)
        
        self.test_semen_source(user_id, pig_farm_id)
        
        print('\n\nTest Summary')
        pprint.pprint(self.summary)
        
  
        
if __name__ == '__main__':
    t = TestAPIAccount()
    
    t.test_auto_clean_data(1, "Jackson Farm", "Punod Farm")