# August 17, 2025
# Jack Wong

import os
import sys


from datetime               import datetime, timedelta

sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import requests
import random
import json
import string
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
},


{
    'name': 'Rennie Requistas',
    'address_level_1_id':  ADRS_LEVEL_1_ID_CEBU_PROV,
    'address_level_2_id':  ADRS_LEVEL_2_ID_TALISAY,
    'address_level_3_id':  ADRS_LEVEL_3_ID_TABUNOC,
    'contact_number':   '0920345987',
    'whatsapp':         '08796900234',
    'messenger':    'Rennie Requistas'
},





]



def generate_random_string(length):
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits
    # Generate the random string by choosing 'length' characters
    random_string = ''.join(random.choices(characters, k=length))
    return random_string



def write_summary_to_file(summary):
    s = json.dumps(summary, indent=4)

    cur_directory   = os.getcwd()
    abspath         = os.path.join(cur_directory, 'test_summary_acc.json')
        
    file = open(abspath, 'w')
    s = file.write(s)
    file.close()



PIG_OPERATION_TYPE_GESTATING        = 1
PIG_OPERATION_TYPE_LACTATING_PIGLETS        = 2
PIG_OPERATION_TYPE_GROWING          = 3

class TestBase:
    def __init__(self, business_object, summary):
        self.business_object    = business_object
        self.summary            = summary
        
        self.url_add            = '%s%s/add'    %(BASE_URL, business_object)
        self.url_update         = '%s%s/update' %(BASE_URL, business_object)
        
        
    def set_url_add(self, url_add):
        self.url_add = url_add
    
    
    def request_add(self, data, input_checks = None):
        """
        input_checks : list of dictionary
            [
                {'input':'uhid', 'type':'str', 'cannot_be_empty': 1, 'test_random': 1}
            ]
        """
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
        
        if input_checks is not None:
            
            for cur_entry in input_checks:
                cur_entry_type = cur_entry['type']
                if cur_entry_type == 'str':
                    
                    values = cur_entry['input']
                    print ('\n\nTesting input check; invalid input: %s') % values
                    
                    if 'test_random' in cur_entry:
                        
                        cur_data = copy.copy(data)
                        cur_data[cur_entry['input']] = generate_random_string(6)
                        res_json = self._request_add_send(cur_data)
                        
                        result_num  = res_json['result']['num']
                        assert(result_num > 0)
                    
                    if 'cannot_be_empty' in cur_entry:
                        cur_data = copy.copy(data)
                        cur_data[cur_entry['input']] = ''
                        res_json = self._request_add_send(cur_data)
                        
                        result_num  = res_json['result']['num']
                        assert(result_num > 0)
                    
        
        res_json = self._request_add_send(data)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        pprint.pprint(res_json)
        
        entry_hid   = res_json[self.business_object]['hid']
        
        
        # Some major business objects have different hashids salt.
        if self.business_object == 'account':
            res_decrypt = hashids_account.decrypt(entry_hid)
        else:
            res_decrypt = hashids_common.decrypt(entry_hid)
        
        entry_id    = res_decrypt[0]
            
        print(f"{self.business_object}.id = {entry_id}")
        assert(entry_id > 0)
        
        # Need to add back entry hid to data for update test
        key = self.business_object + '_hid'
        data[key] = entry_hid

        if self.business_object not in self.summary:
            self.summary[self.business_object] = {}
            
        if self.business_object not in self.summary:
            self.summary[self.business_object] = {}
            
        self.summary[self.business_object]['add'] = 'OK'
        
        write_summary_to_file(self.summary)
        
        return res_json
    
    
    def _request_add_send(self, data):
        values = (self.business_object, self.url_add)
        print('\n***** Testing add %s; url = %s ; data' % values)
        pprint.pprint(data)
        
        r = requests.post(self.url_add, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        return res_json
    
    
    def test_duplicate_add(self, data):
        values = (self.business_object, self.url_add )
        s = '\n\n***** Testing duplicate adding %s; url = %s; data' %values
        pprint.pprint(data)
        
        r = requests.post(self.url_add, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
 
        if self.business_object == 'account':
            assert(res_json['result']['code'] == 'RES_NUM_ACCOUNT_ALREADY_REGISTERED_FOR_USER')
        else:
            assert(res_json['result']['code'] == 'RES_NUM_DUPLICATE_ENTRY')
        
        self.summary[self.business_object]['add_duplicate_check'] = 'OK'
        
        write_summary_to_file(self.summary)
        

    def request_update(self, data):
        
        values = (self.business_object, self.url_update)
        print('\n\n*****  Testing update %s; url = %s ; data' % values)
        pprint.pprint(data)
        
        r = requests.post(self.url_update, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result = ")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        self.summary[self.business_object]['update'] = 'OK'
        
        write_summary_to_file(self.summary)
    
    
    def request_delete(self, url):
        values = (self.business_object, url)
        print('\n\n***** Testing delete %s; url = %s ' % values)
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        self.summary[self.business_object]['delete'] = 'OK'
        
        write_summary_to_file(self.summary)
    
    
    def request_list(self, url):
        
        values = (self.business_object, url)
        print('\n\n****** Testing get_list %s; url = %s' % values)
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
    
        len_items = len(res_json['data'])
        assert(len_items > 0)
        
        self.summary[self.business_object]['list'] = 'OK'
        
        write_summary_to_file(self.summary)
        
        return res_json
        

class TestAccount(TestBase):
    def __init__(self, summary):
        super().__init__('account', summary)
        
        # Overwrite default url_add
        self.url_add    = BASE_URL + 'account/register'
        
    
    def test_register(self, user_id, acc_name):
        user_uhid       = hashids_user.encrypt(user_id)
        
        data = {
            "uhid":         user_uhid,
            "name":         acc_name,
            "country_id":   1
        }
        
        
        res_json = self.request_add(data)
        
        if 'account_hid' in data:
            
            self.summary['account']['account_hid'] = data['account_hid']
            self.summary['account']['register'] = 'OK'
        
        return data
        
        
    def test_update(self, data):
        # Test account update
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        data['name']    = data['name'] + dt_now_s
        
        self.request_update(data)
        
    
    def test_get_usergroups(self, account_hid):
        print(f"\n\n***** Testing get account user groups; account_hid = {account_hid}")
        url = BASE_URL + 'user_group/list?ahid=' + account_hid
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        len_items = len(res_json['data'])
        assert(len_items == 3)
        
        self.summary['account']['user_groups_list'] = 'OK'
        
    
class TestFeedBrand(TestBase):
    def __init__(self, summary):
        super().__init__('feed_brand', summary)
    
    
    def test_add(self, user_id, name):
        user_uhid   = hashids_user.encrypt(user_id)
            
        data = {
            "uhid":         user_uhid,
            "name":         name
        }

        
        input_checks = [
            {'input':'uhid', 'type':'str',  'test_random': 1},
            {'input':'name', 'type':'str', 'cannot_be_empty': 1}
        ]


        res_json = self.request_add(data, input_checks)
        return data
    
    

class TestFeedSupplier(TestBase):
    def __init__(self, summary):
        super().__init__('feed_supplier', summary)
        

    def test_add(self, user_id):
        user_uhid   = hashids_user.encrypt(user_id)
            
        data = {
            "uhid":         user_uhid,
            "name":         'Ayan Sampan',
            "address_level_1_id":   ADRS_LEVEL_1_ID_CEBU_PROV,
            "address_level_2_id":   ADRS_LEVEL_2_ID_NAGA,
            "address_level_3_id":   ADRS_LEVEL_3_ID_TAGJAGUIMIT
        }

        input_checks = [
            {'input':'uhid', 'type':'str',  'test_random': 1},
            {'input':'name', 'type':'str', 'cannot_be_empty': 1}
        ]

        res_json = self.request_add(data)
        return data
        
        
    def test_update(self, data):
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        data['name']    = data['name'] + dt_now_s
        
        self.request_update(data)
        
        
    def test_get_list(self, address_level_2_id):
        url = BASE_URL + 'feed_supplier/list?address_level_2_id=%s' % address_level_2_id
        return self.request_list(url)
    

class TestSemenSupplier(TestBase):
    def __init__(self, summary):
        super().__init__('semen_supplier', summary)
        
    
    def test_add(self, user_id):
        user_uhid   = hashids_user.encrypt(user_id)
        
        data = {
            "uhid":         user_uhid,
            "name":                 'Growbest Agrivet',
            "address_level_1_id":   ADRS_LEVEL_1_ID_CEBU_PROV,
            "address_level_2_id":   ADRS_LEVEL_2_ID_ARGAO
        }
        
        res_json = self.request_add(data)
        return data
        
    
    def test_update(self, data):
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        data['name']    = data['name'] + dt_now_s
              
        self.request_update(data)
    
    
    def test_get_list(self, address_level_1_id):
        url = BASE_URL + 'semen_supplier/list?address_level_1_id=' + address_level_1_id 
        return self.request_list(url)
        

class TestPigRaceLine(TestBase):
    def __init__(self, summary):
        super().__init__('pig_race_line', summary)

    



class TestAccountPigBuyer(TestBase):
    def __init__(self, summary):
        super().__init__('account_pig_buyer', summary)
        
    
    def test_add(self, user_id, num_entries = 2):
        user_uhid       = hashids_user.encrypt(user_id)
        
        len_items       = len(RANDOM_PIG_BUYERS)
        
        count           = 0
        
        taken_index     = []
        
        result          = []
        
        while count < num_entries:
            index = random.randint(0, len_items-1)
            
            # Be sure num_entries < len(RANDOM_PIG_BUYERS)
            if index in taken_index:
                continue
                
            taken_index.append(index)
        
            data = copy.copy(RANDOM_PIG_BUYERS[index])
            data['uhid'] = user_uhid
            
            count += 1
        
            res_json = self.request_add(data)
            
            result.append(data)
            
        return result
    
    
    def test_update(self, data):
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        data['name']    = data['name'] + dt_now_s
        
        self.request_update(data)
    

class TestAccountPigOps(TestBase):
    def __init__(self, summary):
        super().__init__('account_pig_ops', summary)
    
    
    def test_add(self, user_id, operation_type):
        user_uhid       = hashids_user.encrypt(user_id)
        
        
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


        print(f'*****  Testing adding account_pig_ops; operation_type ={s_type}')
      
        res_json = self.request_add(data)
        
        return data
        
        
        
    def test_update(self, data):
        # Test account_pig_ops update
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        data['name']    = data['name'] + dt_now_s
        
        self.request_update(data)
        

class TestFarmStaff(TestBase):
    def __init__(self, summary):
        self.business_object = 'farm_staff'
        super().__init__(self.business_object, summary)
        
    
    def test_add(self, user_id, pig_farm_id, num_entries = 3):
        user_uhid       = hashids_user.encrypt(user_id)
        pig_farm_hid    = hashids_common.encrypt(pig_farm_id)
        
        len_items       = len(RANDOM_STAFF_NAMES)
        
        count           = 0
        
        taken_index     = []
        
        result          = []
        
        while count < num_entries:
            index           = random.randint(0, len_items-1)
            
            # Be sure num_entries < len(RANDOM_STAFF_NAMES)
            if index in taken_index:
                continue
                
            index = taken_index.append(index)
            
            staff_name      = RANDOM_STAFF_NAMES[index]
            
            data = {
                "uhid":                 user_uhid,
                "pig_farm_hid":         pig_farm_hid,
                "name":                 staff_name
            }
            
            self.request_add(data)
            
            result.append(data)
            
            count += 1
        
        return result
        
        
    def test_update(self, data):
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y%m%d_%H%M%S')
        
        data['name']    = data['name'] + dt_now_s
              
        self.request_update(data)
        
    

class TestAPIAccount:
    def __init__(self):
        self.account_hid = None
        
        self.summary    = None
        self.load_previous_test_summary()
    
    
    def load_previous_test_summary(self):
        cur_directory   = os.getcwd()
        abspath         = os.path.join(cur_directory, 'test_summary_acc.json')
        
        if os.path.exists(abspath):
            file = open(abspath, 'r')
            s = file.read()
            file.close()
            
            try:
                self.summary = json.loads(s)
            except Exception as e:
                print("\n\nCannot parse to json: %s" % abspath)
                print("Error: %s" % str(e))
            
            
        if self.summary is None:
            self.summary    = {}
                
            
    
    def test_account_register(self, user_id, acc_name):
        t = TestAccount(self.summary)
        
        data_input = t.test_register(user_id, acc_name)
        
        t.test_duplicate_add(data_input)
    
        t.test_update(data_input)
            
        
        account_hid = data_input['account_hid']
        
        res = hashids_account.decrypt(account_hid)
        account_id = res[0]
            
        t.test_get_usergroups(account_hid)
        
        
        self.test_account_pig_buyer(user_id)
        
        
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
        
        t.test_duplicate_add(data_input)
        
        t.test_update(data_input)
        
        address_level_1_id = ADRS_LEVEL_1_ID_CEBU
        t.test_get_list(address_level_1_id)


    def test_feed_brand(self, user_id):
        t = TestFeedBrand(self.summary)
        data_input = t.test_add(user_id, 'Promix')
        
        data_input = t.test_add(user_id, 'UltraPack')
        
        
        t.test_duplicate_add(data_input)
        
        
        # Test get_list feed_brand
        url = BASE_URL + 'feed_brand/list?inc_deleted=1&inc_user_audit=1'
        t.request_list(url)
    
    
    def test_feed_supplier(self, user_id):
        t = TestFeedSupplier(self.summary)
        data_input = t.test_add(user_id)
        
        t.test_duplicate_add(data_input)
        
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
        
        
    def test_pig_farm_staff(self, user_id, pig_farm_id, num_entries = 3):
        t = TestFarmStaff(self.summary)
        
        list_data_input = t.test_add(user_id, pig_farm_id, num_entries)
        data_input      = list_data_input[0] # get the first entry
        pig_farm_hid    = data_input['pig_farm_hid']
        
        t.test_duplicate_add(data_input)
        
        t.test_update(data_input)
        
        # Delete last entry
        data_delete = list_data_input[num_entries - 1]
        user_uhid   = data_delete['uhid']
        entry_hid   = data_delete['pig_farm_staff_hid']
        
        # Test delete pig_farm_staff
        values = (user_uhid, entry_hid)
        url = BASE_URL + 'pig_farm_staff/delete?uhid=%s&ehid=%s' % values
        
        t.request_delete(url)
        
        
        # Test get_list pig_farm_staff
        url = BASE_URL + 'pig_farm_staff/list?pfhid=' + pig_farm_hid + '&inc_deleted=1&inc_user_audit=1'
        t.request_list(url)
        
        
    def test_account_pig_ops(self, user_id, operation_type):
        t = TestAccountPigOps(self.summary)
        
        data_input = t.test_add(user_id, operation_type)
        
        t.test_duplicate_add(data_input)
        
        t.test_update(data_input)
        
        
        # Test delete account_pig_ops
        data_delete = data_input
        user_uhid   = data_delete['uhid']
        entry_hid   = data_delete['account_pig_ops_hid']
        
        values = (user_uhid, entry_hid)
        url = BASE_URL + 'account_pig_ops/delete?uhid=%s&ehid=%s' % values
        
        t.request_delete(url)
        
        # Test get_list account_pig_ops
        account_hid = self.summary['account']['account_hid']
        
        values  = (account_hid , operation_type)
        url = BASE_URL + 'account_pig_ops/list?ahid=%s&operation_type=%s&inc_deleted=1&inc_user_audit=1' % values
        t.request_list(url)
        
        
    def test_account_pig_buyer(self, user_id, num_entries = 2):
        t = TestAccountPigBuyer(self.summary)
        
        list_data_input = t.test_add(user_id, num_entries)
        data_input      = list_data_input[0] # get the first entry
        
        t.test_duplicate_add(data_input)
        
        t.test_update(data_input) 
        
        
        # Delete last entry
        data_delete = list_data_input[num_entries - 1]
        user_uhid   = data_delete['uhid']
        entry_hid   = data_delete['account_pig_buyer_hid']
        
        # Test delete account_pig_buyer
        values = (user_uhid, entry_hid)
        url = BASE_URL + 'account_pig_buyer/delete?uhid=%s&ehid=%s' % values
        
        t.request_delete(url)
        
        
        account_hid = self.summary['account']['account_hid']
        
        # Test get_list account_pig_buyer
        url = BASE_URL + 'account_pig_buyer/list?ahid=' + account_hid + '&inc_deleted=1&inc_user_audit=1'
        t.request_list(url)
        
        
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
        values = (user_uhid, new_pig_race_line_hid)
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