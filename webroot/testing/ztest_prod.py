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
    def test_pig_prod_add(self, user_id, sow_id, insem_type = 'B'):
        user_uhid   = hashids_user.encrypt(user_id)
        
        sow_hid     = hashids_user.encrypt(sow_id)
        
        
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
        
        if insem_type == 'B':
            url = BASE_URL + 'sow_boar/list?pfhid=' + pfhid + '&sex=M&order_by=1'
        
        r = requests.get(url)
        res_text = str(r.text)
        res_json = json.loads(res_text)
        
        
        now             = datetime.now()
        now_ts          = now.strftime('%Y-%m-%d %H:%M:%S')
        print(f"\n\n#################  {now_ts}  ###########################")
        
        
 
        
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
        
    
        
if __name__ == '__main__':
    t = TestAPIAccount()
    
    t.test_auto_clean_data(1, "Jackson Farm", "Punod Farm")