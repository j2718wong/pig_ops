# February 2, 2026
# Jack Wong

import os
import sys
import pprint


from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse


from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import data_model           as dm


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)


from r_a0_security_checks   import check_if_valid_user_account
from r_utils                import remove_database_null_description



  

@app.post("/pf_feed_buy/add", tags=["Pig Farm"])
async def pig_farm_feed_buy_add(request: Request, data: dm.DataPigFarmFeedBuy):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    pig_farm_hid        = data.pig_farm_hid
    
    res = hashids_common.decrypt(pig_farm_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PF_FEED_BUY_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_PF_FEED_BUY_INVALID_PIG_FARM_HASHID'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
        
        return result
        
    pig_farm_id = res[0]

    
    feed_supplier_hid        = data.feed_supplier_hid
    
    res = hashids_common.decrypt(feed_supplier_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PF_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID,
                'code': 'ERROR_PF_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
        
        return result
        
    feed_supplier_id = res[0]
    
    
    
    
    
    data.user_id           = user_id
    data.pig_farm_id       = pig_farm_id
    data.feed_supplier_id  = feed_supplier_id
    
    res_add    =  model['pf_feed_buy'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    
    # remove plain id
    cur_id      = res_add['pf_feed_buy']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del res_add['pf_feed_buy']['id']
    res_add['pf_feed_buy']['hid'] = cur_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)

    
    return res_add
    
    
@app.post("/pf_feed_buy/update", tags=["Pig Farm"])
async def pig_farm_feed_buy_update(request: Request, data: dm.DataPigFarmFeedBuy):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    pf_feed_buy_hid = data.pf_feed_buy_hid
    
    
    res = hashids_common.decrypt(pf_feed_buy_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_INVALID_HASHID'
            }
        }
    
    pf_feed_buy_id = res[0]
    
    
    feed_supplier_hid        = data.feed_supplier_hid
    
    res = hashids_common.decrypt(feed_supplier_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PF_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID,
                'code': 'ERROR_PF_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
        
        return result
        
    feed_supplier_id = res[0]
    
    
    
    data.user_id   = user_id
    data.pf_feed_buy_id = pf_feed_buy_id
    data.feed_supplier_id  = feed_supplier_id
    
    res_update    =  model['pf_feed_buy'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    cur_id      = res_update['pf_feed_buy']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del res_update['pf_feed_buy']['id']
    res_update['pf_feed_buy']['hid'] = cur_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)

        
    return res_update
    
    
def replace_plain_ids_feed_item(cur_entry):
    cur_id  = cur_entry['feed_item']['id']
    cur_hid = hashids_common.encrypt(cur_id)
    
    del cur_entry['feed_item']['id']
    cur_entry['feed_item']['hid']   = cur_hid
    
    
    cur_id  = cur_entry['feed_type']['id']
    cur_hid = hashids_common.encrypt(cur_id)
    
    del cur_entry['feed_type']['id']
    cur_entry['feed_type']['hid']   = cur_hid
    
    
    cur_id  = cur_entry['feed_brand']['id']
    cur_hid = hashids_common.encrypt(cur_id)
    
    del cur_entry['feed_brand']['id']
    cur_entry['feed_brand']['hid']   = cur_hid
    
    
    
@app.get("/pf_feed_buy/list", tags=["Pig Farm"])
async def pf_feed_buy_list(request: Request, pfhid: str, page_number = 1, 
        date_since = None):
    """
    Will get pig farm feed_buy list.
    
    Parameters
    ----------
    
    pfhid:str
        pig_farm hashid

        
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_FEED_BUY_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_PIG_FARM_HASHID'
            }
        }
        
        return result
        
    pig_farm_id = res[0]


    res = model['pf_feed_buy'].get_list(pig_farm_id, 
        page_number = page_number, 
        date_since = date_since)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    

    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['pf_feed_buy']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pf_feed_buy']['id']
        cur_entry['pf_feed_buy']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['feed_supplier']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['feed_supplier']['id']
        cur_entry['feed_supplier']['hid']   = cur_hid
        
        
        for cur_item in cur_entry['feed_items']:
            replace_plain_ids_feed_item(cur_item)
            
    
    # Get pig_farm.feed_buy data_ver_num data_ver_num
    pig_farm_ver_num = model['pig_farm'].get_data_ver_num(pig_farm_id)
    
    data_ver_num = {
        'pig_farm':{
            'feed_buy': pig_farm_ver_num['data_ver_num']['feed_buy']
        }
    }
    
            
    return {
        'result':{
            'num':  0
        },
        
        'data': res,
        
        'data_ver_num': data_ver_num
    }
    
