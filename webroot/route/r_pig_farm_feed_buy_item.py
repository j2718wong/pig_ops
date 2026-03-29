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

from r_pig_farm_feed_buy    import replace_plain_ids_feed_item

  

@app.post("/pf_feed_buy_item/add", tags=["Pig Farm"])
async def pig_farm_feed_buy_item_add(request: Request, 
        data: dm.DataPigFarmFeedBuyItem):
    
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
                'code': 'ERROR_USER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    pig_farm_feed_buy_hid        = data.pig_farm_feed_buy_hid
    
    res = hashids_common.decrypt(pig_farm_feed_buy_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PF_FEED_BUY_ITEM_INVALID_FEED_BUY_HASHID,
                'code': 'ERROR_PF_FEED_BUY_ITEM_INVALID_FEED_BUY_HASHID'
            }
        }
        
        
        return result
        
    pig_farm_feed_buy_id = res[0]

    
    feed_type_hid        = data.feed_type_hid
    
    res = hashids_common.decrypt(feed_type_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PF_FEED_BUY_ITEM_INVALID_FEED_TYPE_HASHID,
                'code': 'ERROR_PF_FEED_BUY_ITEM_INVALID_FEED_TYPE_HASHID'
            }
        }
        
        
        return result
        
    feed_type_id = res[0]
    
    
    feed_brand_hid        = data.feed_brand_hid
    
    res = hashids_common.decrypt(feed_brand_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PF_FEED_BUY_ITEM_INVALID_FEED_BRAND_HASHID,
                'code': 'ERROR_PF_FEED_BUY_ITEM_INVALID_FEED_BRAND_HASHID'
            }
        }
        
        
        return result
        
    feed_brand_id = res[0]
    
    
    
    
    data.user_id              = user_id
    
    data.pig_farm_feed_buy_id  = pig_farm_feed_buy_id
    data.feed_type_id          = feed_type_id
    data.feed_brand_id         = feed_brand_id
    
    res_add    =  model['pf_feed_buy_item'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    
    # remove plain id
    cur_id      = res_add['feed_buy_item']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del res_add['feed_buy_item']['id']
    res_add['feed_buy_item']['hid'] = cur_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)

    
    return res_add
    
    
@app.post("/pf_feed_buy_item/update", tags=["Pig Farm"])
async def pig_farm_feed_buy_item_update(request: Request, 
        data: dm.DataPigFarmFeedBuyItem):
    
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
    
    
    
    pf_feed_buy_item_hid = data.pf_feed_buy_item_hid

    res = hashids_common.decrypt(pf_feed_buy_item_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PF_FEED_BUY_ITEM_INVALID_HASHID,
                'code': 'ERROR_PF_FEED_BUY_ITEM_INVALID_HASHID'
            }
        }
    
    
    pf_feed_buy_item_id = res[0]
    
    
    feed_type_hid        = data.feed_type_hid
    
    res = hashids_common.decrypt(feed_type_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PF_FEED_BUY_ITEM_INVALID_FEED_TYPE_HASHID,
                'code': 'ERROR_PF_FEED_BUY_ITEM_INVALID_FEED_TYPE_HASHID'
            }
        }
        
        
        return result
        
    feed_type_id = res[0]
    
    
    feed_brand_hid        = data.feed_brand_hid
    
    res = hashids_common.decrypt(feed_brand_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PF_FEED_BUY_ITEM_INVALID_FEED_BRAND_HASHID,
                'code': 'ERROR_PF_FEED_BUY_ITEM_INVALID_FEED_BRAND_HASHID'
            }
        }
        
        
        return result
        
    feed_brand_id = res[0]
    
    
    
    
    data.user_id              = user_id
    data.pf_feed_buy_item_id  = pf_feed_buy_item_id
    data.feed_type_id         = feed_type_id
    data.feed_brand_id        = feed_brand_id
    
    res_update    =  model['pf_feed_buy_item'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    cur_id      = res_update['feed_buy_item']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del res_update['feed_buy_item']['id']
    res_update['feed_buy_item']['hid'] = cur_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
    
    return res_update
    

@app.get("/pf_feed_buy_item/list", tags=["Pig Farm"])
async def pig_farm_feed_buy_item_list(request: Request, pf_feed_buy_hid: str):
    """
    Will get pig farm feed_buy item list.
    
    Parameters
    ----------
    
    pf_feed_buy_hid:str
        pig_farm  feed_buy hashid

        
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_common.decrypt(pf_feed_buy_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_FEED_BUY_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_PIG_FARM_HASHID'
            }
        }
        
        return result
        
    pf_feed_buy_id = res[0]


    res = model['pf_feed_buy'].get_list_items(pf_feed_buy_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    

    
    # Replace plain id
    for cur_entry in res:
        replace_plain_ids_feed_item(cur_entry)
        
        
            
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }

