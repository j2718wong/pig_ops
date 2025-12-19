# August 9, 2025
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import data_model           as dm



@app.post("/account/selection/add", tags=["Account"])
async def account_selection_add(selection_data: dm.DataAccountSelection):
    uhid    = selection_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_SELECTION_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_SELECTION_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]

    
    feed_supplier_id    = 0
    semen_supplier_id   = 0
    
    feed_supplier_hid =  selection_data.feed_supplier_hid
    if feed_supplier_hid is not None:
        res = hashids_common.decrypt(feed_supplier_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_SELECTION_INVALID_FEED_SUPPLIER_HASHID,
                    'code': 'ERROR_ACCOUNT_SELECTION_INVALID_FEED_SUPPLIER_HASHID',
                    'desc': ''
                }
            }
        
        feed_supplier_id = res[0]
    

    semen_supplier_hid = selection_data.semen_supplier_hid
    if semen_supplier_hid is not None:
        res = hashids_common.decrypt(semen_supplier_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_SELECTION_INVALID_SEMEN_SUPPLIER_HASHID,
                    'code': 'ERROR_ACCOUNT_SELECTION_INVALID_SEMEN_SUPPLIER_HASHID',
                    'desc': ''
                }
            }
        
        semen_supplier_id = res[0]
    
    
    
    selection_data.user_id              = user_id
    selection_data.feed_supplier_id     = feed_supplier_id
    selection_data.semen_supplier_id    = semen_supplier_id
    
        
    res_add =  model['account'].add_account_selection(selection_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    
    if res_add['result']['num'] == 0:
    
        if feed_supplier_id > 0:
            list_ids = [feed_supplier_id]
            
            res_suppliers = model['feed_supplier'].get_list(list_ids = list_ids, 
                minimum_info = 0)
            feed_supplier = res_suppliers[0]
            
            #Replace Plain Id
            cur_id      = feed_supplier['feed_supplier']['id']
            cur_hid     = hashids_common.encrypt(cur_id)
            
            del feed_supplier['feed_supplier']['id']
            feed_supplier['feed_supplier']['hid']   = cur_hid
            
            
            get_location_address_names_and_replace_ids(feed_supplier)
        
            result = {
                'num':  0,
                'code': 'SUCCESS',
                'desc': ''
            }
            
            feed_supplier['result'] = result
            
            return feed_supplier
            
    
    
    cur_id      = res_add['account']['id']
    cur_hashid  = hashids_account.encrypt(cur_id)
    
    # remove plain id
    del res_add['account']['id']
    res_add['account']['hid'] = cur_hashid

        
    return res_add
    


def get_account_lookup_selection(account_id, sel_f_brand = 0, 
        sel_f_supplier = 0, sel_s_supplier = 0):
            
    res_f_brand = []
    if sel_f_brand > 0:
        res = model['account'].get_business_obj_selection(account_id, 
            BUSINESS_OBJ_ID_FEED_BRAND)
    
        res_f_brand = [hashids_common.encrypt(cur_id) for cur_id in res] if res else []
    
    
    res_f_supplier = []
    if sel_f_supplier > 0:
        res = model['account'].get_business_obj_selection(account_id, 
            BUSINESS_OBJ_ID_FEED_SUPPLIER)
    
        res_f_supplier = [hashids_common.encrypt(cur_id) for cur_id in res] if res else []
    
    res_s_supplier = []
    if sel_s_supplier > 0:
        res = model['account'].get_business_obj_selection(account_id, 
            BUSINESS_OBJ_ID_SEMEN_SUPPLIER)
    
        res_s_supplier = [hashids_common.encrypt(cur_id) for cur_id in res] if res else []
    
    return {
        'f_brand':      res_f_brand,
        'f_supplier':   res_f_supplier,
        's_supplier':   res_s_supplier
    }
    
 
@app.get("/account/selection", tags=["Account"])
async def account_selection(ahid: str, sel_f_brand: int = 0, sel_f_supplier: int = 0,
        sel_s_supplier: int = 0):
    """
    Will get account_selection

    Parameters
    ----------
    ahid : str
        account hashid
    
    
    """
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_SELECTION_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_SELECTION_INVALID_HASHID',
                'desc': ''
            }
        }
    
    
    account_id = res[0]
    
    
    res = get_account_lookup_selection(account_id, sel_f_brand, 
            sel_f_supplier, sel_s_supplier) 
    
    
    return {
            'result':{
                'num':  0,
                'code': 'SUCCESS',
                'desc': ''
            },
            
            'account_lookup': res
        }
    


@app.post("/account/selection/delete", tags=["Account"])
async def account_selection_delete(selection_data: dm.DataAccountSelection):
    uhid    = selection_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_SELECTION_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_SELECTION_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    feed_brand_id       = None
    feed_supplier_id    = None 
    semen_supplier_id   = None
    
    feed_brand_hid = selection_data.feed_brand_hid
    if feed_brand_hid is not None:
        res = hashids_common.decrypt(feed_brand_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_SELECTION_INVALID_FEED_BRAND_HASHID,
                    'code': 'ERROR_ACCOUNT_SELECTION_INVALID_FEED_BRAND_HASHID',
                    'desc': ''
                }
            }
        
        feed_brand_id = res[0]
    
    
    feed_supplier_hid = selection_data.feed_supplier_hid
    if feed_supplier_hid is not None:
        res = hashids_common.decrypt(feed_supplier_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_SELECTION_INVALID_FEED_SUPPLIER_HASHID,
                    'code': 'ERROR_ACCOUNT_SELECTION_INVALID_SUPPLIER_HASHID',
                    'desc': ''
                }
            }
        
        feed_supplier_id = res[0]
    
    
    semen_supplier_hid = selection_data.semen_supplier_hid
    if semen_supplier_hid is not None:
        res = hashids_common.decrypt(semen_supplier_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_SELECTION_INVALID_FEED_SUPPLIER_HASHID,
                    'code': 'ERROR_ACCOUNT_SELECTION_INVALID_SUPPLIER_HASHID',
                    'desc': ''
                }
            }
        
        semen_supplier_id = res[0]
    
    
     
    selection_data.user_id              = user_id
    selection_data.feed_brand_id        = feed_brand_id    
    selection_data.feed_supplier_id     = feed_supplier_id  
    selection_data.semen_supplier_id    = semen_supplier_id
    
    res_delete = model['account_selection'].delete(selection_data)
    
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    cur_id      = res_delete['account']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    # remove plain id
    del res_delete['account']['id']
    res_delete['account']['hid'] = cur_hid
        
    return res_delete
    
