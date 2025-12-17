# August 17, 2025
# Jack Wong

import sys


from datetime               import datetime, timedelta


from common_constants       import *
from common_app             import *
from common_fast_api        import *


import requests
import random
import json
import pprint




BASE_URL = 'http://localhost:8080/'

    



class TestBase:
    def __init__(self, user_id):
        self.summary        = {}
        
        self.data_test      = self.get_init_data(user_id)
        
        
        
    def get_init_data(self, user_id):
        
        user_uhid      = hashids_user.encrypt(user_id)
        
         
        # Get user_info
        url = BASE_URL + 'user/info?uhid=' + user_uhid
        
        print(f'\n\n****** GET user_info; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
     
    
        data            = res_json['data']
        
        account_hid     = data['user']['account_hid']
        res             = hashids_account.decrypt(account_hid)
        account_id      = res[0]
        
        
        # Get farm list of user account
        url = BASE_URL + 'pig_farm/list?ahid=' + account_hid
        
        print(f'\n\n****** GET user.account farm_list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)

        
        list_pig_farm   = res_json['data']
        len_items       = len(list_pig_farm)
        assert(len_items > 0)
        
        
        # Select pig_farm
        sel_pig_farm    = list_pig_farm[0]
        
        cur_pig_farm    = sel_pig_farm['pig_farm']
        
        
        # Get list of sows in cur_pig_farm
        pfhid           = cur_pig_farm['hid']
        url = BASE_URL + 'sow_boar/list?pfhid=' + pfhid + '&sex=F&order_by=1'
        
    
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        
        list_sow        = res_json['data']
        len_items       = len(list_sow)
        assert(len_items > 0)
        
        print(f"\n\nNumber of sows in {cur_pig_farm['name']} = {len_items}\n\n")
        
        
        # Get list of boars available in the pig_farm
        url = BASE_URL + 'sow_boar/list?pfhid=' + pfhid + '&sex=M&order_by=1'
        
    
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        
        list_boar       = res_json['data']
        len_items       = len(list_boar)
        assert(len_items > 0)
        
        
        
        # Get list of semen sources avaiable for the account
        url = BASE_URL + 'semen_source/list?ahid=' + account_hid
        
        print(f'\n\n****** GET Semen source list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
     
    
        list_semen_source   = res_json['data']
        
        
        
        
        # Get list_staff of the farm
        url = BASE_URL + 'pig_farm_staff/list?pfhid=' + pfhid 
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        
        list_staff      = res_json['data']
        len_list_staff  = len(list_staff)
        assert(len_items > 0)
        
        
        return {
            'user_uhid':        user_uhid,
            'account_hid':      account_hid,
            'account_id':       account_id,
            'pig_farm':         cur_pig_farm,
            'list_sow':         list_sow,
            'list_boar':        list_boar,
            'list_semen_source':list_semen_source,
            'list_staff':       list_staff
        }
        
        
        
        
    def test_pig_prod_add_by_boar(self, user_uhid, pfhid, sow, 
            staff_hid, dt_insem_s):
        
        # Get the list of boars available in the pig_farm
        url = BASE_URL + 'sow_boar/list?pfhid=' + pfhid + '&sex=M&order_by=1'
        
    
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        
        list_boar       = res_json['data']
        len_items       = len(list_boar)
        assert(len_items > 0)
        
        
        index           = random.randint(0, len_items-1)
        cur_boar        = list_boar[index]
        boar_hid        = cur_boar['hid']
        
        sow_hid         = sow['hid']
        
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
    
        url = BASE_URL + 'pig_prod/add'
        
        data = {
            "uhid":                 user_uhid,
            
            "sow_hid":              sow_hid,
            "boar_hid":             boar_hid,
            "insem_cost_comments":  "Takal from " + cur_boar["name"],
            "insem_staff_hid":      staff_hid,
            "date_insemination":    dt_insem_s
        }
        

        print(f'***** Testing adding pig_production via boar insemination; url = {url} ')
        print(f'sow = {sow['name']}; boar = {cur_boar['name']}')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        self.summary['pig_prod']['by_boar']    = {}
        self.summary['pig_prod']['by_boar']['add'] = 'OK'
        
        
        
        pig_prod_hid        = res_json['pig_prod']['hid']
        res_decrypt         = hashids_common.decrypt(pig_prod_hid)
        pig_prod_id    = res_decrypt[0]
        
        print(f"pig_prod_id = {pig_prod_id}")
        assert(pig_prod_id > 0)
        
        
        data['pig_prod_hid']    = pig_prod_hid
        
        
        return data
        
    
    def _test_pig_prod_add_by_ai(self, user_uhid, account_id, sow,
            staff_hid, dt_insem_s, use_internal_semen = 0):
        
        account_hid = hashids_account.encrypt(account_id)
        
        url = BASE_URL + 'semen_source/list?ahid=' + account_hid
        
        print(f'\n\n****** GET Semen source list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
     
    
        data            = res_json['data']
        
        list_internal_semen = []
        list_external_semen = []
        
        for cur_entry in data:
            if 'boar' in cur_entry:
                list_internal_semen.append(cur_entry)
                
            if 'external_semen' in cur_entry:
                list_external_semen.append(cur_entry)
                
        
        len_items_internal = len(list_internal_semen)
        len_items_external = len(list_external_semen)
        
        if use_internal_semen > 0:
            assert(len_items_internal > 0)
            list_semen_source = list_internal_semen
        else:
            assert(len_items_external > 0)
            list_semen_source = list_external_semen
        
        
        len_items       = len(list_semen_source)
        
        index           = random.randint(0, len_items-1)
        cur_semen_source = list_semen_source[index]
        semen_source_hid = cur_semen_source['hid']
        
        sow_hid         = sow['hid']
        
        
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {dt_now_s}  ###########################")
        
    
        url = BASE_URL + 'pig_prod/add'
        
        data = {
            "uhid":                 user_uhid,
            
            "sow_hid":              sow_hid,
            "semen_source_hid":     semen_source_hid,
            "insem_cost_comments":  "AI from " + cur_semen_source["name"],
            "insem_staff_hid":      staff_hid,
            "date_insemination":    dt_insem_s
        }
        

        print(f'***** Testing adding pig_production via artificial insemination; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        self.summary['pig_prod']['by_ai']    = {}
        self.summary['pig_prod']['by_ai']['add'] = 'OK'
        
        
        
        pig_prod_hid        = res_json['pig_prod']['hid']
        res_decrypt         = hashids_common.decrypt(pig_prod_hid)
        pig_prod_id    = res_decrypt[0]
        
        print(f"pig_prod_id = {pig_prod_id}")
        assert(pig_prod_id > 0)
        
        
        data['pig_prod_hid']    = pig_prod_hid
        
        
        return data
        
    
        