# August 29, 2025
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import data_model           as dm

   
@app.post("/prod_feed_bal/add")
async def prod_feed_bal_add(prod_feed_bal_data: dm.DataProdFeedBal):
    uhid    = prod_feed_bal_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_bal_INVALID_USER_HASHID,
                'code': 'ERROR_PROD_FEED_bal_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_prod_hid        = prod_feed_bal_data.pig_prod_hid
    pig_prod_id         = 0
    
    if pig_prod_hid is not None:
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PROD_FEED_bal_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PROD_FEED_bal_INVALID_PIG_PROD_HASHID',
                    'desc': ''
                }
            }
        
        pig_prod_id = res[0]
        
    
    pig_prod_group_hid  = prod_feed_bal_data.pig_prod_group_hid
    pig_prod_group_id   = 0
    
    if pig_prod_group_hid is not None:
        res = hashids_common.decrypt(pig_prod_group_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PROD_FEED_bal_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PROD_FEED_bal_INVALID_PIG_PROD_HASHID',
                    'desc': ''
                }
            }
        
        pig_prod_group_hid = res[0]
    

    
    prod_feed_bal_data.user_id          = user_id
    prod_feed_bal_data.pig_prod_id      = pig_prod_id
    prod_feed_bal_data.pig_prod_group_id= pig_prod_group_id
    
    res_add    =  model['prod_feed_bal'].add(prod_feed_bal_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    prod_feed_bal_id    = res_add['prod_feed_bal']['id']
    prod_feed_bal_hid   = hashids_common.encrypt(prod_feed_bal_id)
    
    # remove plain id
    del res_add['prod_feed_bal']['id']
    res_add['prod_feed_bal']['hid'] = prod_feed_bal_hid

        
    return res_add
    

@app.post("/prod_feed_bal/update")
async def prod_feed_bal_update(prod_feed_bal_data: dm.DataProdFeedBal):
    uhid    = prod_feed_bal_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_bal_INVALID_USER_HASHID,
                'code': 'ERROR_PROD_FEED_bal_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    prod_feed_balance_hid    = prod_feed_bal_data.prod_feed_balance_hid
    
    res = hashids_common.decrypt(prod_feed_balance_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_bal_INVALID_FEED_BRAND_HASHID,
                'code': 'ERROR_PROD_FEED_bal_INVALID_FEED_BRAND_HASHID',
                'desc': ''
            }
        }
    
    prod_feed_balance_id = res[0]
    
    
    prod_feed_bal_data.user_id          = user_id
    prod_feed_bal_data.prod_feed_bal_id = prod_feed_balance_id
   
    
    res_update    =  model['prod_feed_bal'].update(prod_feed_bal_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['prod_feed_bal']['id']
    res_update['prod_feed_bal']['hid'] = prod_feed_bal_hid
        
    return res_update
 
    
@app.get("/prod_feed_bal/list")
async def prod_feed_bal_list(pig_prod_hid: str, inc_user_audit:int = 0):
    """
    Will get prod_feed_bal list.
    
    Parameters
    ----------
    
    pig_prod_hid:str
        pig_prod hashid

    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_bal_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_PROD_FEED_bal_INVALID_PIG_PROD_HASHID',
                'desc': ''
            }
        }
    
    
    pig_prod_id = res[0]
        
    res = model['prod_feed_bal'].get_list(pig_prod_id = pig_prod_id, 
            inc_user_audit = inc_user_audit)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    # Replace plain id
    for cur_entry in res:
        prod_feed_bal_id    = cur_entry['feed_bal']['id']
        prod_feed_bal_hid   = hashids_common.encrypt(prod_feed_bal_id)
        
        # remove plain id
        del cur_entry['feed_bal']['id']
        cur_entry['feed_bal']['hid'] = prod_feed_bal_hid
        
        
        feed_type_id        = cur_entry['feed_type']['id']
        feed_type_hid       = hashids_common.encrypt(feed_type_id)
        
        # remove plain id
        del cur_entry['feed_type']['id']
        cur_entry['feed_type']['hid'] = feed_type_hid
        
        
        feed_brand_id       = cur_entry['feed_brand']['id']
        feed_brand_hid      = hashids_common.encrypt(feed_brand_id)
        
        # remove plain id
        del cur_entry['feed_brand']['id']
        cur_entry['feed_brand']['hid'] = feed_brand_hid
        
        
        feed_supplier_id    = cur_entry['feed_supplier']['id']
        feed_supplier_hid   = hashids_common.encrypt(feed_supplier_id)
        
        # remove plain id
        del cur_entry['feed_supplier']['id']
        cur_entry['feed_supplier']['hid'] = feed_supplier_hid
        
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    

    