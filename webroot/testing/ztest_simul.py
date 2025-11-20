# November 19, 2025
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

from ztest_base             import TestBase

BASE_URL = 'http://localhost:8080/'


INSEM_TYPE_BOAR             = 0
INSEM_TYPE_AI               = 1


class SimulProd:
    def __init__(self, data_sow, insem_type):
        
        self.data_sow       = data_sow
        
        self.insem_type     = insem_type
        
        self.list_staff     = None
        
        self.list_boar      = None
        
        self.list_semen_source = None
        
        self.user_hid       = None
        
        
    def run(self):
        dt_now              = datetime.now()
        
        date_of_birth       = self.data_sow['date_of_birth']
        dt_birth            = datetime.strptime(date_insem, '%Y-%m-%d')
        
        """
        Part 1: Insemination simulation 
        """
        
        # Calculate date insemination
        dt_insem            = dt_birth + timedelta(days = 210)
        if dt_insem >= dt_now: 
            return
            
            
        dt_insem_s      = dt_insem.strftime('%Y-%m-%d')
            
        # Get staff
        len_staff       = len(self.list_staff)
        index           = random.randint(0, len_staff-1)
        cur_staff       = self.list_staff[index]
           
           
        pig_prod_hid    = None
            
        if self.insem_type == INSEM_TYPE_BOAR:
            # Get Boar
            len_items       = len(self.list_boar)
            index           = random.randint(0, len_items-1)
            cur_boar        = self.list_boar[index]
            
            res = self._pig_prod_add_by_boar(cur_boar, cur_staff, dt_insem_s)
            pig_prod_hid    = res['pig_prod_hid']
        
        else:
            # Get Semen Source
            len_items       = len(self.list_semen_source)
            index           = random.randint(0, len_items-1)
            cur_semen_source= self.list_semen_source[index]
            
            res = self._pig_prod_add_by_ai(cur_semen_source, cur_staff, dt_insem_s)
            pig_prod_hid = res['pig_prod_hid']
            
            
        """
        Part 2: Gestating Ops simulation 
        """
        list_gestating_ops = self._get_pig_prod_ops(pig_prod_hid, 
                PIG_OPERATION_TYPE_GESTATING)
        
        for cur_entry in list_gestating_ops:
            date_target     = cur_entry['pig_prod_pig_ops']['date_target']
            dt_target       = datetime.strptime(date_target, '%Y-%m-%d')
            
            # Add 30% random chance to add 1 day to target
            index           = random.randint(0, 9)
            if index >= 7:
                dt_target   = dt_target + timedelta(days=1)
            
            if dt_target >= dt_now: 
                return
            
            dt_target_s     = dt_target.strftime('%Y-%m-%d')
            
            account_pig_ops = cur_entry['account_pig_ops']
            
            
            pig_prod_pig_ops_hid = cur_entry['pig_prod_pig_ops']['hid']
            
            index           = random.randint(0, len_staff-1)
            cur_staff       = self.list_staff[index]
            staff_hid       = cur_staff['hid']

               
            notes = 'Updated ' + account_pig_ops['name']
               
            self._update_pig_prod_ops(pig_prod_pig_ops_hid, staff_hid, 
                        dt_target_s, notes)
    
        
        """
        Part 3: Update pig prod birth simulation 
        """
        random_num_days = random.randint(0, 4)
        num_days = 112 + random_num_days
        dt_actual_birth = dt_insem + timedelta(days = num_days)
        
        if dt_actual_birth > dt_now:
            return
            
        self._update_pig_prod_birth(pig_prod_hid, staff_hid, date_birth)
        
        
    def _pig_prod_add_by_boar(self, boar, staff, date_insem):
        url = BASE_URL + 'pig_prod/add'
        
        data = {
            "uhid":                 self.user_uhid,
            
            "sow_hid":              self.data_sow['hid'],
            "boar_hid":             boar['hid'],
            "insem_notes":          "Takal from " + boar['name'],
            "insem_staff_hid":      staff['hid'],
            "insem_date":           date_insem
        }
        

        print(f'***** Testing adding pig_production via boar insemination; url = {url} ')
        print(f'sow = {sow['name']}; boar = {boar['name']}')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        if 'pig_prod' not in self.summary:
            self.summary['pig_prod'] = {}
            
        if 'by_boar' not in self.summary['pig_prod']:
            self.summary['pig_prod']['by_boar']    = {}
        
        self.summary['pig_prod']['by_boar']['add'] = 'OK'
        
        
        
        pig_prod_hid        = res_json['pig_prod']['hid']
        res_decrypt         = hashids_common.decrypt(pig_prod_hid)
        pig_prod_id         = res_decrypt[0]
        
        print(f"pig_prod_id = {pig_prod_id}")
        assert(pig_prod_id > 0)
        
        
        data['pig_prod_hid']    = pig_prod_hid
        
        return data
        
    
    def _pig_prod_add_by_ai(self, semen_source, staff, date_insem):
        url = BASE_URL + 'pig_prod/add'
        
        data = {
            "uhid":                 self.user_uhid,
            
            "sow_hid":              self.data_sow['hid'],
            "semen_source_hid":     seme_source['hid'],
            "insem_notes":          "AI from " + cur_semen_source["name"],
            "insem_cost":           200.0,
            "semen_cost":           1500.0,
            "insem_staff_hid":      staff['hid'],
            "insem_date":           date_insem
        }
        

        print(f'***** Testing adding pig_production via artificial insemination; url = {url} ')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        if 'pig_prod' not in self.summary:
            self.summary['pig_prod'] = {}
            
        if 'by_boar' not in self.summary['pig_prod']:
            self.summary['pig_prod']['by_boar']    = {}
        
        self.summary['pig_prod']['by_ai']['add'] = 'OK'
        
        
        
        pig_prod_hid        = res_json['pig_prod']['hid']
        res_decrypt         = hashids_common.decrypt(pig_prod_hid)
        pig_prod_id         = res_decrypt[0]
        
        print(f"pig_prod_id = {pig_prod_id}")
        assert(pig_prod_id > 0)
        
        
        data['pig_prod_hid']    = pig_prod_hid
        
        return data
    
    
    def _get_pig_prod_ops(self, pig_prod_hid, operation_type):
        values = (pig_prod_hid, operation_type)
        url = BASE_URL + 'pig_prod_pig_ops/list?prod_hid=%s&operation_type=%s' %(values)
        
        print(f'\n\n****** GET pig_prod_pig_ops list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
     
    
        result  = res_json['data']
        
        return result
    
    
    def _update_pig_prod_ops(self, pig_prod_pig_ops_hid, staff_hid, date_update,
                notes):
                    
        url = BASE_URL + 'pig_prod_pig_ops/update'
        
        data = {
            "uhid":                 self.user_uhid,
            "pig_prod_pig_ops_hid": pig_prod_pig_ops_hid,
            "staff_hid":            staff_hid,
            
            "date":                 date_update,
            "notes":                notes
        }
            
            
        print(f"\n\n***** Testing pig_prod_ops update; url = {url} ; data")
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        result_num = res_json['result']['num']
        
        if before_birth > 0:
            assert(result_num == 0)
        else:
            assert(result_num > 0)
        
        self.summary['pig_prod']['pig_prod_ops']['update'] = 'OK'
        
        
    def _update_pig_prod_birth(self, pig_prod_hid, staff_hid, date_birth):
        
        total_pigs      = 11 + random.randint(0, 5)
        num_pigs_dead   = random.randint(0, 1)
        
        remaining_pigs  = total_pigs - num_pigs_dead
        
        num_pigs_male   = int(remaining_pigs/2 - random.randint(0, 2))
        num_pigs_female = remaining_pigs - num_pigs_male
    
        
        url = BASE_URL + 'pig_prod/update_birth'
        
        
        data_birth = {
            "uhid":                 self.user_uhid,
            "pig_prod_hid":         pig_prod_hid,
            "birth_staff_hid":      staff_hid,
            
            "date_actual_birth":    date_birth,
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
        
        self.summary['pig_prod']['update_birth'] = 'OK'
        
    
        return data_birth
    

class TestSimul(TestBase):
    def __init__(self):
        super.__init__()
        
        
    def run(self):
        
        for cur_entry in self.data_test['list_sow']:
            
            
            
    def 
    