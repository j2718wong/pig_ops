# August 29, 2025
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

   
@app.post("/feed_buy/add", tags=["Production Details"])
async def feed_buy_add(request: Request, data: dm.DataFeedBuy):
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
                'num':  ERROR_FEED_BUY_INVALID_USER_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    pig_prod_hid        = data.pig_prod_hid
    pig_prod_id         = 0
    
    if pig_prod_hid is not None:
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_FEED_BUY_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_FEED_BUY_INVALID_PIG_PROD_HASHID'
                }
            }
        
        pig_prod_id = res[0]
        
    
    pig_prod_group_hid  = data.pig_prod_group_hid
    pig_prod_group_id   = 0
    
    if pig_prod_group_hid is not None:
        res = hashids_common.decrypt(pig_prod_group_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_FEED_BUY_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_FEED_BUY_INVALID_PIG_PROD_HASHID'
                }
            }
        
        pig_prod_group_hid = res[0]
    
        
    feed_type_hid    = data.feed_type_hid
    
    res = hashids_common.decrypt(feed_type_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BUY_INVALID_FEED_TYPE_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_FEED_TYPE_HASHID'
            }
        }
    
    feed_type_id = res[0]
    
    
    feed_brand_hid    = data.feed_brand_hid
    
    res = hashids_common.decrypt(feed_brand_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BUY_INVALID_FEED_BRAND_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_FEED_BRAND_HASHID'
            }
        }
    
    feed_brand_id = res[0]
    
    
    feed_supplier_hid    = data.feed_supplier_hid
    
    res = hashids_common.decrypt(feed_supplier_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID'
            }
        }
    
    feed_supplier_id = res[0]
    
    
    
    data.user_id          = user_id
    data.pig_prod_id      = pig_prod_id
    data.pig_prod_group_id= pig_prod_group_id
    data.feed_type_id     = feed_type_id
    data.feed_brand_id    = feed_brand_id
    data.feed_supplier_id = feed_supplier_id
    
    res_add    =  model['feed_buy'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    feed_buy_id    = res_add['feed_buy']['id']
    feed_buy_hid   = hashids_common.encrypt(feed_buy_id)
    
    # remove plain id
    del res_add['feed_buy']['id']
    res_add['feed_buy']['hid'] = feed_buy_hid

        
    return res_add
    

@app.post("/feed_buy/update", tags=["Production Details"])
async def feed_buy_update(request: Request, data: dm.DataFeedBuy):
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
                'num':  ERROR_FEED_BUY_INVALID_USER_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    feed_buy_hid    = data.feed_buy_hid
    
    res = hashids_common.decrypt(feed_buy_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BUY_INVALID_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_HASHID'
            }
        }
    
    feed_buy_id = res[0]
    
    
    data.user_id           = user_id
    data.feed_buy_id       = feed_buy_id
    
    
    res_update    =  model['feed_buy'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['feed_buy']['id']
    res_update['feed_buy']['hid'] = feed_buy_hid
        
    return res_update
    
    
"""
@app.get("/feed_buy/delete", tags=["Production Details"])
async def feed_buy_delete(request: Request, uhid:str, ehid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BUY_INVALID_USER_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(ehid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BUY_INVALID_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_HASHID'
            }
        }
    
    feed_buy_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'feed_buy_id':     feed_buy_id
    }
    
    
    res_delete    =  model['feed_buy'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['feed_buy']['id']
    res_delete['feed_buy']['hid'] = ehid
        
    return res_delete
"""

    
@app.get("/feed_buy/list", tags=["Production Details"])
async def feed_buy_list(request: Request, pig_prod_hid: str, inc_user_audit:int = 0):
    """
    Will get feed_buy list.
    
    Parameters
    ----------
    
    pig_prod_hid:str
        pig_prod hashid

    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BUY_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_PIG_PROD_HASHID'
            }
        }
    
    
    pig_prod_id = res[0]
        
    res = model['feed_buy'].get_list(pig_prod_id = pig_prod_id, 
            inc_user_audit = inc_user_audit)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # Replace plain id
    for cur_entry in res:
        cur_id      = cur_entry['feed_buy']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['feed_buy']['id']
        cur_entry['feed_buy']['hid'] = cur_hid
        
        
        cur_id      = cur_entry['feed_type']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['feed_type']['id']
        cur_entry['feed_type']['hid'] = cur_hid
        
        
        cur_id      = cur_entry['feed_brand']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['feed_brand']['id']
        cur_entry['feed_brand']['hid'] = cur_hid
        
        
        cur_id      = cur_entry['feed_supplier']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['feed_supplier']['id']
        cur_entry['feed_supplier']['hid'] = cur_hid
        
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    
    

    
