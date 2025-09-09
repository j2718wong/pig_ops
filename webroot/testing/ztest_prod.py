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

    



DEFAULT_FEED_UNIT_COST = {
    'GESTATING':    1460.0,
    'LACTATING':    1670.0,
    'PRESTARTER':   1600.0,
    'STARTER':      1850.0,
    'GROWER':       1700.0,
    'FINISHER':     1575.0
}



        
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
            pig_prod_id     = hashids_common.decrypt(pig_prod_hid)[0]
            
            data_insem = self._test_pig_prod_update_insem(data_add)
            
            if count_sow < 2:
                self._test_pig_prod_gestating_ops(user_uhid, pig_prod_hid, staff_hid,
                    before_birth = 1)
                    
                self._test_prod_lactating_ops(user_uhid, pig_prod_hid, staff_hid, 
                    after_birth = 0)
                
            
            # update birth
            data_birth = self._test_prod_update_birth(data_add)
            
            notes = "Nanganak anay " + cur_sow['name']
            self._test_pig_prod_notes_add(user_uhid, pig_prod_hid, notes)
                
            
            if count_sow < 2:
                # This is a datetime object
                dt_birth    = data_birth['dt_birth']
                
                num_days_random = random.randint(2, 25)
                dt_dead     = dt_birth + timedelta(days = num_days_random)
                dt_dead_s   = dt_dead.strftime('%Y-%m-%d')
                
                index_sex   = random.randint(0, 1)
                sex         = 'M' if index_sex == 0 else 'F'
                
                data_pig_dead = {
                    "uhid":                 user_uhid,
                    "pig_prod_hid":         pig_prod_hid,
                               
                    "date_dead":            dt_dead_s,
                    "dead_type_id":         1,
                    "sex":                  sex,
                    "comments":             "Namatay baktin"
                }
                
                res_add = self._test_prod_pig_dead_add(data_pig_dead)
                
                
                data_pig_dead['comments'] =  data_pig_dead['comments'] + ' updated'
                
                self._test_prod_pig_dead_update(data_pig_dead)
                
                
                # Test again if it will give correct error message
                self._test_pig_prod_gestating_ops(user_uhid, pig_prod_hid, staff_hid,
                    before_birth = 0)
                
                self._test_prod_lactating_ops(user_uhid, pig_prod_hid, staff_hid, 
                    after_birth = 1)
            
            
            # Test buy lactating feed
            data_feed_buy = {'uhid': user_uhid, 'pig_prod_hid': pig_prod_hid}
            self._test_prod_feed_buy_add(account_id, pig_prod_id, 
                    FEED_TYPE_ID_LACTATING, data_feed_buy)
            
            
            # Test buy prestarter feed
            data_feed_buy = {'uhid': user_uhid, 'pig_prod_hid': pig_prod_hid}
            self._test_prod_feed_buy_add(account_id, pig_prod_id, 
                    FEED_TYPE_ID_PRESTARTER, data_feed_buy)
            
            
            # Test buy starter feed
            data_feed_buy = {'uhid': user_uhid, 'pig_prod_hid': pig_prod_hid}
            self._test_prod_feed_buy_add(account_id, pig_prod_id, 
                    FEED_TYPE_ID_STARTER, data_feed_buy)
            
            
            self._test_prod_update_weaning(data_birth)
            
            notes = "Lutas anay " + cur_sow['name']
            res = self._test_pig_prod_notes_add(user_uhid, pig_prod_hid, notes)
            
            print('adding prod_notes')
            pprint.pprint(res)
        
            pig_prod_notes_hid = res['pig_prod_notes']['hid']
            notes = notes + " updated"
            self._test_pig_prod_notes_update(user_uhid, pig_prod_notes_hid, notes)
            
            
            # Test buy grower feed
            data_feed_buy = {'uhid': user_uhid, 'pig_prod_hid': pig_prod_hid}
            self._test_prod_feed_buy_add(account_id, pig_prod_id, 
                    FEED_TYPE_ID_GROWER, data_feed_buy)
            
            # Test buy finisher feed
            data_feed_buy = {'uhid': user_uhid, 'pig_prod_hid': pig_prod_hid}
            self._test_prod_feed_buy_add(account_id, pig_prod_id, 
                    FEED_TYPE_ID_FINISHER, data_feed_buy)
            
           
            count_sow = count_sow + 1
        
        
        
    def _test_pig_prod_notes_add(self, user_uhid, pig_prod_hid, notes):
        url = BASE_URL + 'pig_prod_notes/add'
        
        data = {
            "uhid":                 user_uhid,
            
            "pig_prod_hid":         pig_prod_hid,
            "notes":                notes
        }

        print(f'\n\n***** Testing adding pig_prod_notes; url = {url} ')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        self.summary['pig_prod']['prod_notes'] = {}
        self.summary['pig_prod']['prod_notes']['add'] = 'OK'
        
        return res_json
        
            
    def _test_pig_prod_notes_update(self, user_uhid, pig_prod_notes_hid, notes):
        url = BASE_URL + 'pig_prod_notes/update'
        
        data = {
            "uhid":                 user_uhid,
            
            "pig_prod_notes_hid":   pig_prod_notes_hid,
            "notes":                notes
        }

        print(f'\n\n***** Testing updating pig_prod_notes; url = {url} ')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        self.summary['pig_prod']['prod_notes']['update'] = 'OK'
        
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
        
        self.summary['pig_prod']['update_birth'] = 'OK'
        
        
        data_birth['dt_birth'] = dt_birth
    
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
        
        
        print(f"\n\n***** Testing pig_prod_update_weaning; url = {url} ; data")
        pprint.pprint(data_weaning)
        
        r = requests.post(url, json = data_weaning)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        result_num = res_json['result']['num']
        assert(result_num == 0)
        
        self.summary['pig_prod']['update_weaning'] = 'OK'
        
    
    def _test_prod_pig_dead_add(self, data):
        url = BASE_URL + 'prod_pig_dead/add'
        
        print(f'\n\n***** Testing pig_prod_pig_dead add; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        result_num = res_json['result']['num']
        assert(result_num == 0)
        
        pig_prod_pig_dead_hid = res_json['pig_prod_pig_dead']['hid']
        
        
        
        
        data['pig_prod_pig_dead_hid'] = pig_prod_pig_dead_hid
        
        self.summary['pig_prod']['pig_dead'] = {}
        self.summary['pig_prod']['pig_dead']['add'] = 'OK'
        
        return data
        
    
    def _test_prod_pig_dead_update(self, data):
        url = BASE_URL + 'prod_pig_dead/update'
        
        print(f'\n\n***** Testing pig_prod_pig_dead update; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        result_num = res_json['result']['num']
        assert(result_num == 0)
        
        pig_prod_pig_dead_hid  = res_json['pig_prod_pig_dead']['hid']
        
        data['pig_prod_pig_dead_hid'] = pig_prod_pig_dead_hid
        
        self.summary['pig_prod']['pig_dead'] = {}
        self.summary['pig_prod']['pig_dead']['add'] = 'OK'
        
        return data
    
    
    def _test_pig_prod_gestating_ops(self, user_uhid, pig_prod_hid, staff_hid, 
            before_birth = 1):
        
        values = (pig_prod_hid, PIG_OPERATION_TYPE_GESTATING)
        url = BASE_URL + 'pig_prod_pig_ops/list?prod_hid=%s&operation_type=%s' %(values)
        
        print(f'\n\n****** GET pig_prod_pig_ops list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
     
    
        list_gestating_ops          = res_json['data']
        
        
        gest_ops_to_update = None
        # Find the gestating_ops that has a name of 'Inject Iron'
        for cur_entry in list_gestating_ops:
            if cur_entry['account_pig_ops']['name'] == 'Inject Iron':
                gest_ops_to_update = cur_entry
                break
                
        if gest_ops_to_update is None:
            return
            
            
        self.summary['pig_prod']['gestating_ops'] = {}
        self.summary['pig_prod']['gestating_ops']['list'] = 'OK' 
        
            
        pig_prod_pig_ops_hid  = gest_ops_to_update['pig_prod_pig_ops']['hid']
        date_update = gest_ops_to_update['pig_prod_pig_ops']['date_target']
        
        
        url = BASE_URL + 'pig_prod_pig_ops/update'
        
        data = {
            "uhid":                 user_uhid,
            "pig_prod_pig_ops_hid": pig_prod_pig_ops_hid,
            "staff_hid":            staff_hid,
            
            "date":     date_update,
            "notes":    "updated gestating ops"
            
        }
            
            
        print(f"\n\n***** Testing prod_gestating_ops update; before_birth = {before_birth}; url = {url} ; data")
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
        
        self.summary['pig_prod']['gestating_ops']['update'] = 'OK'
        
        
    def _test_prod_lactating_ops(self, user_uhid, pig_prod_hid, staff_hid, 
            after_birth = 1):
        
        values = (pig_prod_hid, PIG_OPERATION_TYPE_LACTATING)
        url = BASE_URL + 'pig_prod_pig_ops/list?prod_hid=%s&operation_type=%s' % values
        
        print(f'\n\n****** GET prod_lactating_ops list; url = {url} ')
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
     
    
        list_lactating_ops          = res_json['data']
        
        
        lact_ops_to_update = None
        # Find the lactating_ops that has a name of 'Inject Iron_2'
        for cur_entry in list_lactating_ops:
            if cur_entry['account_pig_ops']['name'] == 'Inject Iron_2':
                lact_ops_to_update = cur_entry
                break
                
        if lact_ops_to_update is None:
            return
            
            
        self.summary['pig_prod']['lactating_ops'] = {}
        self.summary['pig_prod']['lactating_ops']['list'] = 'OK' 
        
            
        pig_prod_pig_ops_hid  = lact_ops_to_update['pig_prod_pig_ops']['hid']
        date_update = lact_ops_to_update['pig_prod_pig_ops']['date_target']
        
        
        url = BASE_URL + 'pig_prod_pig_ops/update'
        
        data = {
            "uhid":                 user_uhid,
            "pig_prod_pig_ops_hid": pig_prod_pig_ops_hid,
            "staff_hid":            staff_hid,
            
            "date":     date_update,
            "notes":    "updated lactating ops"
            
        }
            
            
        print(f"\n\n***** Testing prod_lactating_ops update; after_birth = {after_birth}; url = {url} ; data")
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        result_num = res_json['result']['num']
        
        if after_birth > 0:
            assert(result_num == 0)
        else:
            assert(result_num > 0)
        
        self.summary['pig_prod']['lactating_ops']['update'] = 'OK'
        
    
    def _test_prod_feed_buy_add(self, account_id, pig_prod_id, feed_type_id, data):
        
        feed_type_hid = hashids_common.encrypt(feed_type_id)
        
        # Get feed_supplier selection of account
        
        account_hid = hashids_account.encrypt(account_id)
        
        values = (account_hid, BUSINESS_OBJ_ID_FEED_SUPPLIER)
        url = BASE_URL + 'account/selection?ahid=%s&biz_obj_id=%s' %values
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        
        list_hids  = res_json['data']
        
        if len(list_hids) == 0:
            # randomize feed_supplier
            
            url = BASE_URL + 'feed_supplier/list'
        
            r = requests.get(url)
            res_text = str(r.text)
            res_json = json.loads(res_text)
            
            
            list_feed_suppliers  = res_json['data']
            len_items = len(list_feed_suppliers)
            
            index   = random.randint(0, len_items-1)
            cur_suplier  = list_feed_suppliers[index]
            cur_feed_supplier_hid = cur_suplier['hid']
        
        else:
            index   = random.randint(0, len(list_hids)-1)
            cur_feed_supplier_hid = list_hids[index]
        
        
        
        # Get feed_brand selection of account
        
        values = (account_hid, BUSINESS_OBJ_ID_FEED_BRAND)
        url = BASE_URL + 'account/selection?ahid=%s&biz_obj_id=%s' %values
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        
        list_hids  = res_json['data']
        
        if len(list_hids) == 0:
            # randomize feed_brand
            
            url = BASE_URL + 'feed_brand/list'
        
            r = requests.get(url)
            res_text = str(r.text)
            res_json = json.loads(res_text)
            
            
            list_feed_brands  = res_json['data']
            len_items = len(list_feed_brands)
            
            index   = random.randint(0, len_items-1)
            cur_feed_brand  = list_feed_brands[index]
            cur_feed_brand_hid = cur_feed_brand['hid']
        
        else:
            index   = random.randint(0, len(list_hids)-1)
            cur_feed_brand_hid = list_hids[index]
        
        
        # Get number of sacks feeds already bought for pig_prod
        list_ids =[pig_prod_id]
        res = model['pig_prod'].get_list(list_ids = list_ids)
        
        pig_prod = res[0]
        
        feeds_bought = pig_prod['feeds']['bought']
        
        total_pigs   = pig_prod['pig_production']['cur_pig_count']
        
        
        kg_per_unit = 1
        
        """
        The test process is 
        
        1.) buy lactating feeds once only
        2.) buy prestarter feeds once only
        3.) buy starter feeds once only
        4.) buy grower feeds twice only
        5.) buy grower feeds twice only
        """
        
        
        if feed_type_id == FEED_TYPE_ID_GESTATING:
            kg_per_unit     = DEFAULT_KG_PER_FEED_UNIT['GESTATING']
            cost_per_unit   = DEFAULT_FEED_UNIT_COST['GESTATING']
            
        
        elif feed_type_id == FEED_TYPE_ID_LACTATING:
            kg_per_unit     = DEFAULT_KG_PER_FEED_UNIT['LACTATING']
            cost_per_unit   = DEFAULT_FEED_UNIT_COST['LACTATING']
            num_bought      = feeds_bought['lactating']
            
            if num_bought is None: num_bought = 0
            
            MAX_FEEDS_TO_BUY_LACTATING = 2
            num_feeds_to_buy = MAX_FEEDS_TO_BUY_LACTATING - num_bought
            
            if num_feeds_to_buy == 0:
                return None
            
            
            # Simulate date buy before birth
            production_birth = pig_prod['birth']
            
            if production_birth['date_actual'] is not None:
                date_ref    = production_birth['date_actual']
            else:
                date_ref    = production_birth['date_expected']
                
                
            dt_birth    = datetime.strptime(date_ref, '%Y-%m-%d')
            dt_feed_buy = dt_birth - timedelta(days = 4)
            date_buy    = datetime.strftime(dt_feed_buy, '%Y-%m-%d')
            
            data_feed_buy = {
                'uhid':             data['uhid'],
                
                'pig_prod_hid':     data['pig_prod_hid'],
                'feed_type_hid':    feed_type_hid,
                'feed_brand_hid' :  cur_feed_brand_hid,
                'feed_supplier_hid': cur_feed_supplier_hid,
                'date_buy':         date_buy,
                
                'quantity':         num_feeds_to_buy,
                'kg_per_unit':      int(kg_per_unit),
                
                'unit_cost':        cost_per_unit,
                'total_cost':       num_feeds_to_buy * cost_per_unit
            }
            
            return self._test_prod_feed_buy_add_request(data_feed_buy)
            
        
        elif feed_type_id == FEED_TYPE_ID_PRESTARTER:
            kg_per_unit     = DEFAULT_KG_PER_FEED_UNIT['PRESTARTER']
            cost_per_unit   = DEFAULT_FEED_UNIT_COST['PRESTARTER']
            num_bought      = feeds_bought['prestarter']
            
            if num_bought is None: num_bought = 0
            
            MAX_FEEDS_TO_BUY_PRESTARTER = 1
            
            num_feeds_to_buy = MAX_FEEDS_TO_BUY_PRESTARTER - num_bought
            
            
            if num_feeds_to_buy == 0:
                return None
            
            
            # Simulate date buy 15 days after birth
            production_birth    = pig_prod['birth']
            date_birth  = production_birth['date_actual']
            
            dt_birth    = datetime.strptime(date_birth, '%Y-%m-%d')
            dt_feed_buy = dt_birth + timedelta(days = 15)
            date_buy    = datetime.strftime(dt_feed_buy, '%Y-%m-%d')
            
            data_feed_buy = {
                'uhid':             data['uhid'],
                
                'pig_prod_hid':     data['pig_prod_hid'],
                'feed_type_hid':    feed_type_hid,
                'feed_brand_hid' :  cur_feed_brand_hid,
                'feed_supplier_hid': cur_feed_supplier_hid,
                'date_buy':         date_buy,
                
                'quantity':         num_feeds_to_buy,
                'kg_per_unit':      kg_per_unit,
                
                'unit_cost':        cost_per_unit,
                'total_cost':       num_feeds_to_buy * cost_per_unit
            }
            
            return self._test_prod_feed_buy_add_request(data_feed_buy)
            
            
            
        elif feed_type_id == FEED_TYPE_ID_STARTER:
            kg_per_unit     = DEFAULT_KG_PER_FEED_UNIT['STARTER']
            cost_per_unit   = DEFAULT_FEED_UNIT_COST['STARTER']
            
            num_bought      = feeds_bought['starter']
            
            if num_bought is None: num_bought = 0
            
            MAX_FEEDS_TO_BUY_STARTER = total_pigs
            
            num_feeds_to_buy = MAX_FEEDS_TO_BUY_STARTER - num_bought
            
            
            if num_feeds_to_buy == 0:
                return None
            
            quantity_1 = int(num_feeds_to_buy/2) + random.randint(0,1)
            quantity_2 = num_feeds_to_buy - quantity_1
            
                
            # Buy twice
            production_birth    = pig_prod['birth']
            date_birth  = production_birth['date_actual']
            
            dt_birth    = datetime.strptime(date_birth, '%Y-%m-%d')
            dt_feed_buy = dt_birth + timedelta(days = 40)
            date_buy_1  = datetime.strftime(dt_feed_buy, '%Y-%m-%d')
            
            dt_feed_buy = dt_birth + timedelta(days = 70)
            date_buy_2  = datetime.strftime(dt_feed_buy, '%Y-%m-%d')
            
            data_feed_buy = {
                'uhid':             data['uhid'],
                
                'pig_prod_hid':     data['pig_prod_hid'],
                'feed_type_hid':    feed_type_hid,
                'feed_brand_hid' :  cur_feed_brand_hid,
                'feed_supplier_hid': cur_feed_supplier_hid,
                'date_buy':         date_buy_1,
                
                'quantity':         quantity_1,
                'kg_per_unit':      kg_per_unit,
                
                'unit_cost':        cost_per_unit,
                'total_cost':       quantity_1 * cost_per_unit
            }
            
            self._test_prod_feed_buy_add_request(data_feed_buy)
            
            
            data_feed_buy = {
                'uhid':             data['uhid'],
                
                'pig_prod_hid':     data['pig_prod_hid'],
                'feed_type_hid':    feed_type_hid,
                'feed_brand_hid' :  cur_feed_brand_hid,
                'feed_supplier_hid': cur_feed_supplier_hid,
                'date_buy':         date_buy_2,
                
                'quantity':         quantity_2,
                'kg_per_unit':      kg_per_unit,
                
                'unit_cost':        cost_per_unit,
                'total_cost':       quantity_2 * cost_per_unit
            }
            
            self._test_prod_feed_buy_add_request(data_feed_buy)
            
            
            
        elif feed_type_id == FEED_TYPE_ID_GROWER:
            kg_per_unit     = DEFAULT_KG_PER_FEED_UNIT['GROWER']
            cost_per_unit   = DEFAULT_FEED_UNIT_COST['GROWER']
            
            
            num_bought      = feeds_bought['grower']
            
            if num_bought is None: num_bought = 0
            
            MAX_FEEDS_TO_BUY_GROWER = total_pigs * 2
            
            num_feeds_to_buy = MAX_FEEDS_TO_BUY_GROWER - num_bought
            
            
            if num_feeds_to_buy == 0:
                return None
            
            quantity_1 = int(num_feeds_to_buy/2) + random.randint(0,1)
            quantity_2 = num_feeds_to_buy - quantity_1
            
                
            # Buy twice
            production_birth    = pig_prod['birth']
            date_birth  = production_birth['date_actual']
            
            dt_birth    = datetime.strptime(date_birth, '%Y-%m-%d')
            dt_feed_buy = dt_birth + timedelta(days = 85)
            date_buy_1  = datetime.strftime(dt_feed_buy, '%Y-%m-%d')
            
            dt_feed_buy = dt_birth + timedelta(days = 100)
            date_buy_2  = datetime.strftime(dt_feed_buy, '%Y-%m-%d')
            
            
            data_feed_buy = {
                'uhid':             data['uhid'],
                
                'pig_prod_hid':     data['pig_prod_hid'],
                'feed_type_hid':    feed_type_hid,
                'feed_brand_hid' :  cur_feed_brand_hid,
                'feed_supplier_hid': cur_feed_supplier_hid,
                'date_buy':         date_buy_1,
                
                'quantity':         quantity_1,
                'kg_per_unit':      kg_per_unit,
                
                'unit_cost':        cost_per_unit,
                'total_cost':       quantity_1 * cost_per_unit
            }
            
            self._test_prod_feed_buy_add_request(data_feed_buy)
            
            
            data_feed_buy = {
                'uhid':             data['uhid'],
                
                'pig_prod_hid':     data['pig_prod_hid'],
                'feed_type_hid':    feed_type_hid,
                'feed_brand_hid' :  cur_feed_brand_hid,
                'feed_supplier_hid': cur_feed_supplier_hid,
                'date_buy':         date_buy_2,
                
                'quantity':         quantity_2,
                'kg_per_unit':      kg_per_unit,
                
                'unit_cost':        cost_per_unit,
                'total_cost':       quantity_2 * cost_per_unit
            }
            
            self._test_prod_feed_buy_add_request(data_feed_buy)
            
            
            
        elif feed_type_id == FEED_TYPE_ID_FINISHER:
            kg_per_unit     = DEFAULT_KG_PER_FEED_UNIT['FINISHER']
            cost_per_unit   = DEFAULT_FEED_UNIT_COST['FINISHER']
        
            num_bought      = feeds_bought['finisher']
            
            if num_bought is None: num_bought = 0
            
            MAX_FEEDS_TO_BUY_FINISHER = total_pigs
            
            num_feeds_to_buy = MAX_FEEDS_TO_BUY_FINISHER - num_bought
            
            
            if num_feeds_to_buy == 0:
                return None
                
            quantity_1 = num_feeds_to_buy
        
            production_birth    = pig_prod['birth']
            date_birth  = production_birth['date_actual']
            
            dt_birth    = datetime.strptime(date_birth, '%Y-%m-%d')
            dt_feed_buy = dt_birth + timedelta(days = 110)
            date_buy   = datetime.strftime(dt_feed_buy, '%Y-%m-%d')
          
            data_feed_buy = {
                'uhid':             data['uhid'],
                
                'pig_prod_hid':     data['pig_prod_hid'],
                'feed_type_hid':    feed_type_hid,
                'feed_brand_hid' :  cur_feed_brand_hid,
                'feed_supplier_hid': cur_feed_supplier_hid,
                'date_buy':         date_buy,
                
                'quantity':         quantity_1,
                'kg_per_unit':      kg_per_unit,
                
                'unit_cost':        cost_per_unit,
                'total_cost':       quantity_1 * cost_per_unit
            }
            
            self._test_prod_feed_buy_add_request(data_feed_buy)
            
            
    def _test_prod_feed_buy_add_request(self, data):
        
        url = BASE_URL + 'feed_buy/add'
        
        print(f'\n\n***** Testing pig_prod_feed_buy add; url = {url} ; data')
        pprint.pprint(data)
        
        r = requests.post(url, json = data)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        print(f"\n\nResult; status_code = {r.status_code}; result")
        pprint.pprint(res_json)
 
        result_num = res_json['result']['num']
        assert(result_num == 0)
        
        pig_feed_buy_hid = res_json['feed_buy']['hid']
        
        
        
        
        data['pig_feed_buy_id'] = pig_feed_buy_hid
        
        self.summary['pig_prod']['pig_prod_feed_buy'] = {}
        self.summary['pig_prod']['pig_prod_feed_buy']['add'] = 'OK'
        
        return data
        
    
    def _test_feed_balance_add(self, pig_prod_id):
        test = 1
    
    
if __name__ == '__main__':
    t = TestAPIPigProd()
    
    t.test_pig_prod_add(1)