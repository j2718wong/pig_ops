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

    


        
class TestAPIPigProd:
    def __init__(self):
        self.summary    ={}
    
    
    def test_pig_prod_add(self, user_id):
        user_uhid   = hashids_user.encrypt(user_id)
        
         
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
        cur_pig_farm    = list_pig_farm[0]
        
        
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
        
        # Get staff_list of the farm
        url = BASE_URL + 'pig_farm_staff/list?pfhid=' + pfhid 
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        
        staff_list      = res_json['data']
        len_staff_list  = len(staff_list)
        assert(len_items > 0)
        
        
        self.summary['pig_prod'] = {}
        
        count_sow = 0
        
        INSEM_TYPE_BOAR = 0
        INSEM_TYPE_AI   = 1
        
        cur_insem_type  = INSEM_TYPE_BOAR
        
        for cur_sow in list_sow:
            
            sow_hid     = cur_sow['hid']
            
            # Get random staff
            index           = random.randint(0, len_staff_list-1)
            cur_staff       = staff_list[index]
            staff_hid       = cur_staff['hid']

        
        
            # random insemenation date
            now             = datetime.now()
        
            random_num_days = random.randint(0, 30)
            dt_insem        = now - timedelta(days = (30 + random_num_days))
            dt_insem_s      = dt_insem.strftime('%Y-%m-%d')
        
        
        
            if cur_insem_type == INSEM_TYPE_BOAR:
                data_add = self._test_pig_prod_add_by_boar(user_uhid, pfhid, 
                        cur_sow, staff_hid, dt_insem_s)
                cur_insem_type = INSEM_TYPE_AI
                
            else:
                data_add = self._test_pig_prod_add_by_ai(user_uhid, account_id, 
                        cur_sow, staff_hid, dt_insem_s)
                cur_insem_type = INSEM_TYPE_BOAR
                        
            
            pig_prod_hid    = data_add['pig_prod_hid']
            
            data_insem = self._test_pig_prod_update_insem(data_add)
            data_birth = self._test_prod_update_birth(data_add)
            
            notes = "Nanganak anay " + cur_sow['name']
            self._test_pig_prod_notes_add(user_uhid, pig_prod_hid, notes)
            
            self._test_prod_update_weaning(data_birth)
            
            notes = "Lutas anay " + cur_sow['name']
            res = self._test_pig_prod_notes_add(user_uhid, pig_prod_hid, notes)
            
            print('adding prod_notes')
            pprint.pprint(res)
        
            pig_prod_notes_hid = res['pig_prod_notes']['hid']
            notes = notes + " updated"
            self._test_pig_prod_notes_update(user_uhid, pig_prod_notes_hid, notes)
        
        
    def _test_pig_prod_notes_add(self, user_uhid, pig_prod_hid, notes):
        url = BASE_URL + 'pig_prod_notes/add'
        
        data = {
            "uhid":                 user_uhid,
            
            "pig_prod_hid":         pig_prod_hid,
            "notes":                notes
        }

        print(f'***** Testing adding pig_prod_notes; url = {url} ')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        return res_json
        
            
    def _test_pig_prod_notes_update(self, user_uhid, pig_prod_notes_hid, notes):
        url = BASE_URL + 'pig_prod_notes/update'
        
        data = {
            "uhid":                 user_uhid,
            
            "pig_prod_notes_hid":   pig_prod_notes_hid,
            "notes":                notes
        }

        print(f'***** Testing updating pig_prod_notes; url = {url} ')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        return res_json
        
            
    def _test_pig_prod_add_by_boar(self, user_uhid, pfhid, sow, 
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
        
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {now_ts}  ###########################")
        
    
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
        
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {now_ts}  ###########################")
        
    
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
        
        
    
    def _test_pig_prod_update_insem(self, data_add):
        
        data_add['insemination_cost'] = 100.0
         
        
        # Test pig_prod_update_insem
        url = BASE_URL + 'pig_prod/update_insem'
            
       
        print(f'\n\n***** Testing pig_prod_update_insem; url = {url} ; data_add')
        pprint.pprint(data_add)
        
        r = requests.post(url, json = data_add)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        result_num = res_json['result']['num']
        assert(result_num == 0)
        
        if 'boar_hid' in data_add:
            self.summary['pig_prod']['by_boar']['update_insem'] = 'OK'
        else:
            self.summary['pig_prod']['by_ai']['update_insem'] = 'OK'
        
        
        return data_add
        
        
    def _test_prod_update_birth(self, data_insem):
        date_insemination = data_insem['date_insemination']
        
        dt_insem        = datetime.strptime(date_insemination, '%Y-%m-%d')
        
        dt_birth        = dt_insem + timedelta(days = 115)
        dt_birth_s      = dt_birth.strftime('%Y-%m-%d')
        
        
        total_pigs      = 12 + random.randint(0, 5)
        num_pigs_dead   = random.randint(0, 1)
        
        remaining_pigs  = total_pigs - num_pigs_dead
        
        num_pigs_male   = int(remaining_pigs/2 - random.randint(0, 2))
        num_pigs_female = remaining_pigs - num_pigs_male
    
        
        url = BASE_URL + 'pig_prod/update_birth'
        
        
        data_birth = {
            "uhid":                 data_insem['uhid'],
            "pig_prod_hid":         data_insem['pig_prod_hid'],
            "birth_staff_hid":      data_insem['insem_staff_hid'],
            
            "date_actual_birth":    dt_birth_s,
            "num_pigs_dead":        num_pigs_dead,
            "num_pigs_male":        num_pigs_male,
            "num_pigs_female":      num_pigs_female
        }
        
        
        print(f'\n\n***** Testing pig_prod_update_birth; url = {url} ; data')
        pprint.pprint(data_birth)
        
        r = requests.post(url, json = data_birth)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        result_num = res_json['result']['num']
        assert(result_num == 0)
    
        return data_birth
        
    
    def _test_prod_update_weaning(self, data_birth):
        date_birth      = data_birth['date_actual_birth']
        
        dt_birth        = datetime.strptime(date_birth, '%Y-%m-%d')
        
        dt_weaning      = dt_birth + timedelta(days = 45)
        dt_weaning_s    = dt_weaning.strftime('%Y-%m-%d')
        
        
         
        
        url = BASE_URL + 'pig_prod/update_weaning'
        
        
        data_weaning = {
            "uhid":                 data_birth['uhid'],
            "pig_prod_hid":         data_birth['pig_prod_hid'],
                       
            "date_weaning":         dt_weaning_s,
            "num_pigs_male":        data_birth['num_pigs_male'],
            "num_pigs_female":      data_birth['num_pigs_female']
        }
        
        
        print(f'\n\n***** Testing pig_prod_update_weaning; url = {url} ; data')
        pprint.pprint(data_weaning)
        
        r = requests.post(url, json = data_weaning)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        result_num = res_json['result']['num']
        assert(result_num == 0)
    
    
    
        
if __name__ == '__main__':
    t = TestAPIPigProd()
    
    t.test_pig_prod_add(1)