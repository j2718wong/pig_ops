# November 19, 2025
# Jack Wong

import sys


from datetime               import datetime, timedelta
from collections            import OrderedDict

sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *


from sample_data            import *

import requests
import random
import json
import pprint

from ztest_base             import TestBase

BASE_URL = 'http://localhost:8080/'


INSEM_TYPE_BOAR             = 0
INSEM_TYPE_AI               = 1


# This is based on actual data
FEED_SUPPLIER_PREFERENCE    = [
    {"supplier_name": "Arnel Sampan",
      "supplier_hid": "Q92W83",
      "feed_types": [
        {
            "name":         "GESTATING",
            "unit_weight":  50.0,
            "prices":       [1460.0]
        }, 
        
        {   "name":         "LACTATING", 
            "unit_weight":  50.0,
            "prices":       [1470.0]
        }, 
        
        {   "name":         "BOOSTER", 
            "unit_weight":  10.0,
            "prices":       [750.0]
        },

        {   "name":         "PRE_STARTER", 
            "unit_weight":  25.0,
            "prices":       [1350.0,]
        },
        
        {   "name":         "STARTER", 
            "unit_weight":  50.0,
            "prices":       [1865.0]
        }
        
      ]
    },
    
    {"supplier_name": "Daphne Panonce",
      "supplier_hid": "EKQY8R",
      "feed_types": [
        {     
            "name":         "GROWER",
            "unit_weight":  50.0,
            "prices":       [1650.0]
        },
        
        {
            "name":         "FINISHER",
            "unit_weight":   50.0,
            "prices":       [1525.0]
        }
      ]
    }
    
]


class SimulProd:
    def __init__(self, summary, data_sow, insem_type):
        self.summary        = summary
        
        self.data_sow       = data_sow
        
        self.insem_type     = insem_type
        
        self.list_staff     = None
        
        self.list_boar      = None
        
        self.list_semen_source = None
        
        self.user_uhid       = None
        
        
        self.sow_simul      = None
        
        
    def write_summary_to_file(self,):
        s = json.dumps(self.summary, indent=4)

        cur_directory   = os.getcwd()
        abspath         = os.path.join(cur_directory, 'simul.json')
            
        file = open(abspath, 'w')
        s = file.write(s)
        file.close()
            
        
    def run(self):
        sow_name            = self.data_sow['name']
        if sow_name not in self.summary:
            self.sow_simul = OrderedDict()
            self.summary[sow_name] = self.sow_simul
        else:
            self.sow_simul = OrderedDict(self.summary[sow_name])
        
        dt_now              = datetime.now()
        
        date_of_birth       = self.data_sow['date_of_birth']
        dt_birth            = datetime.strptime(date_of_birth, '%Y-%m-%d')
        
        """
        Part 1: Insemination simulation 
        """
        
        # Calculate date insemination
        dt_insem            = dt_birth + timedelta(days = 210)
        if dt_insem >= dt_now: 
            return
            
            
        dt_insem_s          = dt_insem.strftime('%Y-%m-%d')
            
        # Get staff
        len_staff           = len(self.list_staff)
        index               = random.randint(0, len_staff-1)
        cur_staff           = self.list_staff[index]
           

        pig_prod_hid    = None
        
            
        if 'insem' not in self.sow_simul:
            
            if self.insem_type == INSEM_TYPE_BOAR:
                # Get Boar
                len_items       = len(self.list_boar)
                index           = random.randint(0, len_items-1)
                cur_boar        = self.list_boar[index]
                
                res = self._pig_prod_add_by_boar(cur_boar, cur_staff, dt_insem_s)
                pig_prod_hid    = res['pig_prod_hid']
                
                self.sow_simul['insem'] = {}
                self.sow_simul['insem']['by_boar'] = 'OK'
            
            else:
                # Get Semen Source
                len_items       = len(self.list_semen_source)
                index           = random.randint(0, len_items-1)
                cur_semen_source= self.list_semen_source[index]
                
                res = self._pig_prod_add_by_ai(cur_semen_source, cur_staff, dt_insem_s)
                pig_prod_hid = res['pig_prod_hid']
                
                self.sow_simul['insem'] = {}
                self.sow_simul['insem']['by_ai'] = 'OK'
            
            self.write_summary_to_file()
            
            
        """
        Part 2: Gestating Ops update simulation 
        """
        if 'gestating_pig_ops' not in self.sow_simul:
            
            list_gestating_ops = self._get_pig_prod_ops(pig_prod_hid, 
                    PIG_OPERATION_TYPE_GESTATING)
            
            res = self._update_pig_prod_ops_list(list_gestating_ops, dt_now)
            if res == False: return
            
            
            self.sow_simul['gestating_pig_ops'] = 'OK'
            self.write_summary_to_file()
        
        
        """
        Part 3: Buy lactating feeds few days before expected birth
        """
        
        if 'buy_lacta' not in self.sow_simul:
            random_num_days = random.randint(3, 7)
            num_days = 114 - random_num_days
            dt_buy_lacta = dt_insem - timedelta(days = num_days)
            
            if dt_buy_lacta > dt_now:
                return
            
            dt_buy_lacta = dt_buy_lacta.strftime('%Y-%m-%d')
            
            self._add_feed_buy(pig_prod_hid, 'LACTATING', dt_buy_lacta, 2)
            
            self.sow_simul['buy_lacta'] = 'OK'
            self.write_summary_to_file()
        
        """
        Part 3: Update pig prod birth simulation 
        """
        if 'update_birth' not in self.sow_simul:
            random_num_days = random.randint(0, 4)
            num_days = 112 + random_num_days
            dt_actual_birth = dt_insem + timedelta(days = num_days)
            
            if dt_actual_birth > dt_now:
                return
            
            dt_actual_birth_s = dt_actual_birth.strftime('%Y-%m-%d')
                
            index               = random.randint(0, len_staff-1)
            cur_staff           = self.list_staff[index]
            cur_staff_hid       = cur_staff['hid']
        
            self._update_pig_prod_birth(pig_prod_hid, cur_staff_hid, dt_actual_birth_s)
            
            self.sow_simul['update_birth'] = 'OK'
            self.sow_simul['date_actual_birth'] = dt_actual_birth_s
            self.write_summary_to_file()
            
           
            
        """
        Part 4: Lactating Piglets Ops update simulation 
        """
        if 'lactating_piglets_ops' not in self.sow_simul:
            list_lactating_piglets_ops = self._get_pig_prod_ops(pig_prod_hid, 
                    PIG_OPERATION_TYPE_LACTATING_PIGLETS)
        
            res = self._update_pig_prod_ops_list(list_lactating_piglets_ops, dt_now)
            if res == False: return
            
            
            self.sow_simul['lactating_piglets_ops'] = 'OK'
            self.write_summary_to_file()
            
        
        
        """
        Part 5: Lactating Sow Ops update simulation 
        """
        if 'lactating_sow_ops' not in self.sow_simul:
            list_lactating_sow_ops = self._get_pig_prod_ops(pig_prod_hid, 
                    PIG_OPERATION_TYPE_LACTATING_SOW)
        
            res = self._update_pig_prod_ops_list(list_lactating_sow_ops, dt_now)
            if res == False: return
            
            
            self.sow_simul['lactating_sow_ops'] = 'OK'
            self.write_summary_to_file()
        
            
        
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
        print(f'sow = {self.data_sow['name']}; boar = {boar['name']}')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
        
        result_num  = res_json['result']['num']
        assert(result_num == 0)
        
        
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
    
    
    def _update_pig_prod_ops_list(self, prod_ops_list, dt_now):
        for cur_entry in prod_ops_list:
            date_target     = cur_entry['pig_prod_pig_ops']['date_target']
            dt_target       = datetime.strptime(date_target, '%Y-%m-%d')
            
            # Add 30% random chance to add 1 day to target
            index           = random.randint(0, 9)
            if index >= 7:
                dt_target   = dt_target + timedelta(days=1)
            
            if dt_target >= dt_now: 
                return False
            
            dt_target_s     = dt_target.strftime('%Y-%m-%d')
            
            account_pig_ops = cur_entry['account_pig_ops']
            
            
            pig_prod_pig_ops_hid = cur_entry['pig_prod_pig_ops']['hid']
            
            len_staff       = len(self.list_staff)
            index           = random.randint(0, len_staff-1)
            cur_staff       = self.list_staff[index]
            staff_hid       = cur_staff['hid']

               
            notes = 'Updated ' + account_pig_ops['name']
               
            self._update_pig_prod_ops(pig_prod_pig_ops_hid, staff_hid, 
                        dt_target_s, notes)
        
        return True
        
    
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
        
        assert(result_num == 0)
        
        if 'pig_prod_ops' not in self.sow_simul:
            self.sow_simul['pig_prod_ops'] = {}
            
        self.sow_simul['update'] = 'OK'
        
        
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
        
        
    
        return data_birth
    
    
    def _get_feed_supplier_preference(self, feed_type_name):
        for cur_entry in FEED_SUPPLIER_PREFERENCE:
            for cur_feed_type in cur_entry['feed_types']:
                if cur_feed_type['name'] == feed_type_name:
                    return cur_entry
        return None
        
    
    def _get_feed_type(self, feed_type_name):
        for cur_entry in G_SAMPLE_DATA_FEED_TYPE:
            if cur_entry['name'] == feed_type_name:
                return cur_entry
        return None
    
    
    def _get_supplier_feed_type(self, feed_supplier, feed_type_name):
        for cur_entry in feed_supplier['feed_types']:
            if cur_entry['name'] == feed_type_name:
                return cur_entry
        
        return None
    
    
    def _add_feed_buy(self, pig_prod_hid, feed_type_name, date_buy, quantity):
        feed_type = self._get_feed_type(feed_type_name)
        feed_supplier_pref = self._get_feed_supplier_preference(feed_type_name)
        
        url = BASE_URL + 'feed_buy/add'
        
        preffered_brand_hid = 'Q92W83'  # promix
        
        supplier_feed_type = self._get_supplier_feed_type(feed_supplier_pref, 
                feed_type_name)
        
        unit_weight = supplier_feed_type['unit_weight']
        unit_cost   = supplier_feed_type['prices'][0] # need to improve later
        total_cost  = quantity * unit_cost
        
        data_feed_buy = {
            "uhid":                 self.user_uhid,
            "pig_prod_hid":         pig_prod_hid,
            "feed_type_hid":        feed_type['hid'],
            "feed_brand_hid":       preffered_brand_hid,
            "feed_supplier_hid":    feed_supplier_pref['supplier_hid'],
            
            "date_buy":             date_buy,
            "quantity":             quantity,
            "unit_weight":          unit_weight,
            "unit_cost":            unit_cost,
            "total_cost":           total_cost
            
        }
        
        print(f'\n\n***** Testing feed_buy add; url = {url} ; data')
        pprint.pprint(data_feed_buy)
        
        r = requests.post(url, json = data_feed_buy)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        result_num = res_json['result']['num']
        assert(result_num == 0)
        
        
    
        return data_feed_buy
            
    
"""
Typical data_test 

{
    "user_uhid": "WPG2P2",
    "account_hid": "EG5RPR",
    "account_id": 1,
    "pig_farm": {
        "hid": "Q92W83",
        "flag": 1,
        "name": "Punod Farm20251120_101344"
    },
    "list_sow": [
        {
            "pig_farm_id": 1,
            "farm_sow_id": 1,
            "number": "15871",
            "name": "Nitang",
            "flag": 0,
            "farm_birth_prod_id": 0,
            "last_prod_id": null,
            "status": "Gestating",
            "date_of_birth": "2024-12-30",
            "date_dispose": null,
            "notes": "Added Nitang",
            "dispose_notes": null,
            "dt_entry": "2025-11-20 06:30:40",
            "hid": "Q92W83"
        },
        {
            "pig_farm_id": 1,
            "farm_sow_id": 2,
            "number": "15876",
            "name": "Tasing",
            "flag": 0,
            "farm_birth_prod_id": 0,
            "last_prod_id": null,
            "status": "Gestating",
            "date_of_birth": "2025-02-02",
            "date_dispose": null,
            "notes": "Added Tasing",
            "dispose_notes": null,
            "dt_entry": "2025-11-20 06:30:44",
            "hid": "EKQY8R"
        },
        {
            "pig_farm_id": 1,
            "farm_sow_id": 3,
            "number": "15894",
            "name": "Sita",
            "flag": 0,
            "farm_birth_prod_id": 0,
            "last_prod_id": null,
            "status": "Gestating",
            "date_of_birth": "2025-01-12",
            "date_dispose": null,
            "notes": "Added Sita",
            "dispose_notes": null,
            "dt_entry": "2025-11-20 06:30:48",
            "hid": "0KP5K7"
        },
        {
            "pig_farm_id": 1,
            "farm_sow_id": 4,
            "number": "15910",
            "name": "Diday",
            "flag": 0,
            "farm_birth_prod_id": 0,
            "last_prod_id": null,
            "status": "Gestating",
            "date_of_birth": "2024-12-15",
            "date_dispose": null,
            "notes": "Added Diday",
            "dispose_notes": null,
            "dt_entry": "2025-11-20 06:30:53",
            "hid": "1K7D9J"
        },
        {
            "pig_farm_id": 1,
            "farm_sow_id": 5,
            "number": "15920",
            "name": "Soling",
            "flag": 0,
            "farm_birth_prod_id": 0,
            "last_prod_id": null,
            "status": "Gestating",
            "date_of_birth": "2024-11-29",
            "date_dispose": null,
            "notes": "Added Soling",
            "dispose_notes": null,
            "dt_entry": "2025-11-20 06:30:57",
            "hid": "08DZKQ"
        },
        {
            "pig_farm_id": 1,
            "farm_sow_id": 6,
            "number": "15922",
            "name": "Puring",
            "flag": 0,
            "farm_birth_prod_id": 0,
            "last_prod_id": null,
            "status": "Gestating",
            "date_of_birth": "2024-11-14",
            "date_dispose": null,
            "notes": "Added Puring",
            "dispose_notes": null,
            "dt_entry": "2025-11-20 06:31:01",
            "hid": "M9ZN9G"
        },
        {
            "pig_farm_id": 1,
            "farm_sow_id": 7,
            "number": "15940",
            "name": "Indang",
            "flag": 0,
            "farm_birth_prod_id": 0,
            "last_prod_id": null,
            "status": "Gestating",
            "date_of_birth": "2024-11-10",
            "date_dispose": null,
            "notes": "Added Indang",
            "dispose_notes": null,
            "dt_entry": "2025-11-20 06:31:06",
            "hid": "M8BE8P"
        },
        {
            "pig_farm_id": 1,
            "farm_sow_id": 8,
            "number": "15942",
            "name": "Imyat",
            "flag": 0,
            "farm_birth_prod_id": 0,
            "last_prod_id": null,
            "status": "Gestating",
            "date_of_birth": "2024-10-01",
            "date_dispose": null,
            "notes": "Added Imyat",
            "dispose_notes": null,
            "dt_entry": "2025-11-20 06:31:10",
            "hid": "NKNG81"
        }
    ],
    "list_boar": [
        {
            "pig_farm_id": 1,
            "farm_boar_id": 1,
            "number": "12436",
            "name": "Didoy",
            "flag": 0,
            "farm_birth_prod_id": 0,
            "last_prod_id": null,
            "status": null,
            "date_of_birth": "2025-03-15",
            "date_dispose": null,
            "notes": "Added Didoy",
            "dispose_notes": null,
            "dt_entry": "2025-11-20 06:31:14",
            "hid": "18XJK5"
        },
        {
            "pig_farm_id": 1,
            "farm_boar_id": 2,
            "number": "12449",
            "name": "Gorio",
            "flag": 0,
            "farm_birth_prod_id": 0,
            "last_prod_id": null,
            "status": null,
            "date_of_birth": "2025-02-27",
            "date_dispose": null,
            "notes": "Added Gorio",
            "dispose_notes": null,
            "dt_entry": "2025-11-20 06:31:21",
            "hid": "M86D9R"
        },
        {
            "pig_farm_id": 1,
            "farm_boar_id": 3,
            "number": "12469",
            "name": "Desidido",
            "flag": 0,
            "farm_birth_prod_id": 0,
            "last_prod_id": null,
            "status": null,
            "date_of_birth": "2025-04-18",
            "date_dispose": null,
            "notes": "Added Desidido",
            "dispose_notes": null,
            "dt_entry": "2025-11-20 06:31:25",
            "hid": "E8519Q"
        },
        {
            "pig_farm_id": 1,
            "farm_boar_id": 5,
            "number": "12485",
            "name": "Berto",
            "flag": 0,
            "farm_birth_prod_id": 0,
            "last_prod_id": null,
            "status": null,
            "date_of_birth": "2025-03-02",
            "date_dispose": null,
            "notes": "Added Berto",
            "dispose_notes": null,
            "dt_entry": "2025-11-20 06:31:35",
            "hid": "29GB8Z"
        }
    ],
    "list_semen_source": [
        {
            "pig_farm": {
                "name": "Punod Farm20251120_101344",
                "hid": "Q92W83"
            },
            "flag": 0,
            "boar": {
                "number": "12485",
                "name": "Berto",
                "hid": "29GB8Z"
            },
            "name": "Semen from Butakal - Berto",
            "description": null,
            "dt_entry": "2025-11-20T07:01:17",
            "hid": "Q92W83"
        },
        {
            "pig_farm": {
                "name": "Punod Farm20251120_101344",
                "hid": "Q92W83"
            },
            "flag": 0,
            "external_semen": {
                "supplier_name": "Growbest Agrivet20251119_171215",
                "pig_race_line": {
                    "name": "Camborough 4820251119_171202",
                    "hid": "Q92W83"
                },
                "supplier_hid": "Q92W83"
            },
            "name": "PIC 337",
            "description": null,
            "dt_entry": "2025-11-20T07:01:24",
            "hid": "EKQY8R"
        }
    ],
    "list_staff": [
        {
            "name": "Hilmero20251120_101355",
            "dt_entry": "2025-11-20 02:13:49",
            "hid": "Q92W83"
        },
        {
            "name": "Kevin",
            "dt_entry": "2025-11-20 02:13:51",
            "hid": "EKQY8R"
        }
    ]
}
"""


class TestSimul(TestBase):
    def __init__(self, user_id):
        super().__init__(user_id)
        
        
    def test_simul_sow(self, sow_name):
        cur_sow = None
        for cur_entry in self.data_test['list_sow']:
            if cur_entry['name'] == sow_name:
                cur_sow = cur_entry
                break
                
        cur_simul = SimulProd({}, cur_sow, INSEM_TYPE_BOAR)
        cur_simul.list_staff     = self.data_test['list_staff']
        cur_simul.list_boar      = self.data_test['list_boar']
        cur_simul.list_semen_source = self.data_test['list_semen_source']
        cur_simul.user_uhid      = self.data_test['user_uhid']
        
        cur_simul.run()

        
        
    def run(self):
        # Load simul summary if there is any
        
        
        count = 0
        for cur_entry in self.data_test['list_sow']:
            cur_simul = SimulProd({}, cur_entry, INSEM_TYPE_BOAR)
            cur_simul.list_staff     = self.data_test['list_staff']
            cur_simul.list_boar      = self.data_test['list_boar']
            cur_simul.list_semen_source = self.data_test['list_semen_source']
            cur_simul.user_uhid      = self.data_test['user_uhid']
            
            cur_simul.run()
    
            return
    