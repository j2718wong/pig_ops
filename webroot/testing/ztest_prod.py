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
    
    
    def test_pig_prod_add(self, user_id, sow_id, insem_type = 'B'):
        user_uhid   = hashids_user.encrypt(user_id)
        
        sow_hid     = hashids_common.encrypt(sow_id)
        
        
        # Test user_info
        url = BASE_URL + 'user/info?uhid=' + user_uhid
        
        print(f'\n\n****** GET user_info; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
     
    
        data            = res_json_data
        
        account_hid     = data['user']['account_hid']
        res             = hashids_account.decrypt(account_hid)
        account_id      = res[0]
        
        
        self.summary['pig_prod'] = {}
        
        if insem_type == 'B':
            list_ids = [user_id]
            
            # Get the pig_farm where the sow is located
            sow_info_list = model['sow_boar'].get_list(None, None, inc_disposed = 0, 
                inc_user_audit = 0, list_ids = list_ids, order_by = 0)
            
            sow_info        = sow_info_list[0]
            
            sow_farm_id     = sow_info['pig_farm_id']
            pfhid           = hashids_common.encrypt(sow_farm_id)
            
            
            # Get the list of boars available in the pig_farm
            url = BASE_URL + 'sow_boar/list?pfhid=' + pfhid + '&sex=M&order_by=1'
            
        
            r = requests.get(url)
            res_text = str(r.text)
            res_json = json.loads(res_text)
            
            
            boar_list       = res_json['data']
            len_items       = len(boar_list)
            assert(len_items > 0)
            
            
            index           = random.randint(0, len_items-1)
            cur_boar        = boar_list[index]
            boar_hid        = cur_boar['hid']
            
            # Get staff_list of the farm
            url = BASE_URL + 'pig_farm_staff/list?pfhid=' + pfhid 
            
            r = requests.get(url)
            res_text = str(r.text)
            res_json = json.loads(res_text)
            
            
            staff_list      = res_json['data']
            len_items       = len(staff_list)
            assert(len_items > 0)
            
            
            index           = random.randint(0, len_items-1)
            cur_staff       = staff_list[index]
            staff_id        = cur_staff
            staff_hid       = hashids_common.encrypt(staff_id)
            
            
            now             = datetime.now()
        
            random_num_days = random.randint(0, 30)
            dt_insem        = now - timedelta(days = (30 + random_num_days))
            dt_insem_s      = now.strftime('%Y-%m-%d')
            
        
            now             = datetime.now()
            now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n\n#################  {now_ts}  ###########################")
            
        
            url = BASE_URL + 'pig_prod/add'
            
            data = {
                "uhid":                 user_uhid,
                
                "sow_hid":              sow_hid,
                "boar_hid":             cur_boar,
                "insem_cost_comments":  "Takal from " + cur_boar["name"],
                "insem_staff_hid":      staff_hid,
                "date_insemination":    dt_insem_s
            }
            

            print(f'***** Testing adding pig_production via boar; url = {url} ; data')
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
            
            
            data_insem = self._test_pig_prod_update_insem(data)
            
            data_birth = self._test_prod_update_birth(data)
            
            self._test_prod_update_weaning(data)
    
    
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
        
        if 'boar_id' in data_add:
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
        
        num_pigs_male   = remaining_pigs > 1 - random.randint(0, 2)
        num_pigs_female = remaining_pigs - num_pigs_male
    
        
        url = BASE_URL + 'pig_prod/update_birth'
        
        
        data_birth = {
            "uhid":                 data_insem['uhid'],
            "pig_prod_hid":         data_insem['pig_prod_hid'],
            "birth_staff_hid":      data_insem['insem_staff_hid']
            
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
        
        
         
        
        url = BASE_URL + 'pig_prod/update_birth'
        
        
        data_weaning = {
            "uhid":                 data_birth['uhid'],
            "pig_prod_hid":         data_birth['pig_prod_hid'],
                       
            "date_weaning":         dt_birth_s,
            "num_pigs_male":        num_pigs_male,
            "num_pigs_female":      num_pigs_female
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
    t = TestAPIAccount()
    
    t.test_auto_clean_data(1, "Jackson Farm", "Punod Farm")