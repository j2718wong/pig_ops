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

   
@app.post("/prod_feed_buy/add")
async def prod_feed_buy_add(prod_feed_buy_data: dm.DataProdFeedBuy):
    uhid    = prod_feed_buy_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_BUY_INVALID_USER_HASHID,
                'code': 'ERROR_PROD_FEED_BUY_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_prod_hid        = prod_feed_buy_data.pig_prod_hid
    pig_prod_id         = 0
    
    if pig_prod_hid is not None:
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PROD_FEED_BUY_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PROD_FEED_BUY_INVALID_PIG_PROD_HASHID',
                    'desc': ''
                }
            }
        
        pig_prod_id = res[0]
        
    
    pig_prod_group_hid  = prod_feed_buy_data.pig_prod_group_hid
    pig_prod_group_id   = 0
    
    if pig_prod_group_hid is not None:
        res = hashids_common.decrypt(pig_prod_group_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PROD_FEED_BUY_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PROD_FEED_BUY_INVALID_PIG_PROD_HASHID',
                    'desc': ''
                }
            }
        
        pig_prod_group_hid = res[0]
    
        
    feed_type_hid    = prod_feed_buy_data.feed_type_hid
    
    res = hashids_common.decrypt(feed_type_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_BUY_INVALID_FEED_TYPE_HASHID,
                'code': 'ERROR_PROD_FEED_BUY_INVALID_FEED_TYPE_HASHID',
                'desc': ''
            }
        }
    
    feed_type_id = res[0]
    
    
    feed_brand_hid    = prod_feed_buy_data.feed_brand_hid
    
    res = hashids_common.decrypt(feed_brand_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_BUY_INVALID_FEED_BRAND_HASHID,
                'code': 'ERROR_PROD_FEED_BUY_INVALID_FEED_BRAND_HASHID',
                'desc': ''
            }
        }
    
    feed_brand_id = res[0]
    
    
    feed_supplier_hid    = prod_feed_buy_data.feed_supplier_hid
    
    res = hashids_common.decrypt(feed_supplier_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID,
                'code': 'ERROR_PROD_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID',
                'desc': ''
            }
        }
    
    feed_supplier_id = res[0]
    
    
    
    prod_feed_buy_data.user_id          = user_id
    prod_feed_buy_data.pig_prod_id      = pig_prod_id
    prod_feed_buy_data.pig_prod_group_id= prod_feed_buy_data
    prod_feed_buy_data.feed_type_id     = feed_type_id
    prod_feed_buy_data.feed_brand_id    = feed_brand_id
    prod_feed_buy_data.feed_supplier_id = feed_supplier_id
    
    res_add    =  model['prod_feed_buy'].add(prod_feed_buy_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    prod_feed_buy_id    = res_add['prod_feed_buy']['id']
    prod_feed_buy_hid   = hashids_common.encrypt(prod_feed_buy_id)
    
    # remove plain id
    del res_add['prod_feed_buy']['id']
    res_add['prod_feed_buy']['hid'] = prod_feed_buy_hid

        
    return res_add
    

@app.post("/prod_feed_buy/update")
async def prod_feed_buy_update(prod_feed_buy_data: dm.DataProdFeedBuy):
    uhid    = prod_feed_buy_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_BUY_INVALID_USER_HASHID,
                'code': 'ERROR_PROD_FEED_BUY_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_prod_hid    = prod_feed_buy_data.pig_prod_hid
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_BUY_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_PROD_FEED_BUY_INVALID_PIG_PROD_HASHID',
                'desc': ''
            }
        }
    
    pig_prod_id = res[0]
    
    
    feed_type_hid    = prod_feed_buy_data.feed_type_hid
    
    res = hashids_common.decrypt(feed_type_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_BUY_INVALID_FEED_TYPE_HASHID,
                'code': 'ERROR_PROD_FEED_BUY_INVALID_FEED_TYPE_HASHID',
                'desc': ''
            }
        }
    
    feed_type_id = res[0]
    
    
    feed_brand_hid    = prod_feed_buy_data.feed_brand_hid
    
    res = hashids_common.decrypt(feed_brand_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_BUY_INVALID_FEED_BRAND_HASHID,
                'code': 'ERROR_PROD_FEED_BUY_INVALID_FEED_BRAND_HASHID',
                'desc': ''
            }
        }
    
    feed_brand_id = res[0]
    
    
    feed_supplier_hid    = prod_feed_buy_data.feed_supplier_hid
    
    res = hashids_common.decrypt(feed_supplier_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID,
                'code': 'ERROR_PROD_FEED_BUY_INVALID_FEED_SUPPLIER_HASHID',
                'desc': ''
            }
        }
    
    feed_supplier_id = res[0]
    
    
    prod_feed_buy_data.user_id          = user_id
    prod_feed_buy_data.prod_feed_buy_id = prod_feed_buy_id
    prod_feed_buy_data.pig_prod_id      = pig_prod_id
    prod_feed_buy_data.feed_type_id     = feed_type_id
    prod_feed_buy_data.feed_brand_id    = feed_brand_id
    prod_feed_buy_data.feed_supplier_id = feed_supplier_id
    
    res_update    =  model['prod_feed_buy'].update(prod_feed_buy_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['prod_feed_buy']['id']
    res_update['prod_feed_buy']['hid'] = prod_feed_buy_hid
        
    return res_update
    
    
"""
@app.get("/prod_feed_buy/delete")
async def prod_feed_buy_delete(uhid:str, prod_feed_buy_hid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_BUY_INVALID_USER_HASHID,
                'code': 'ERROR_PROD_FEED_BUY_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(prod_feed_buy_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_BUY_INVALID_HASHID,
                'code': 'ERROR_PROD_FEED_BUY_INVALID_HASHID',
                'desc': ''
            }
        }
    
    prod_feed_buy_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'prod_feed_buy_id':     prod_feed_buy_id
    }
    
    
    res_delete    =  model['prod_feed_buy'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    # remove plain id
    del res_delete['prod_feed_buy']['id']
    res_delete['prod_feed_buy']['hid'] = prod_feed_buy_hid
        
    return res_delete
"""

    
@app.get("/prod_feed_buy/list")
async def prod_feed_buy_list(ahid: str, inc_deleted: int = 0, inc_user_audit:int = 0):
    """
    Will get prod_feed_buy list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid

    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PROD_FEED_BUY_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_PROD_FEED_BUY_INVALID_ACCOUNT_HASHID',
                'desc': ''
            }
        }
    
    
    account_id = res[0]
        
    res = model['prod_feed_buy'].get_list(account_id, 
            inc_deleted, inc_user_audit)
    
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
        cur_id  = cur_entry['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
        
        cur_pig_race_id  = cur_entry['pig_race']['id']
        cur_pig_race_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_race']['id']
        cur_entry['pig_race']['hid']   = cur_hid
        
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    

    