# August 9, 2025
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

@app.post("/account/selection/add", tags=["Account"])
async def account_selection_add(request: Request, data: dm.DataAccountSelection):
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
                'num':  ERROR_ACCOUNT_SELECTION_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_SELECTION_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]

    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    feed_supplier_id    = 0
    semen_supplier_id   = 0
    
    feed_supplier_hid =  data.feed_supplier_hid
    if feed_supplier_hid is not None:
        res = hashids_common.decrypt(feed_supplier_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_SELECTION_INVALID_FEED_SUPPLIER_HASHID,
                    'code': 'ERROR_ACCOUNT_SELECTION_INVALID_FEED_SUPPLIER_HASHID'
                }
            }
        
        feed_supplier_id = res[0]
    

    semen_supplier_hid = data.semen_supplier_hid
    if semen_supplier_hid is not None:
        res = hashids_common.decrypt(semen_supplier_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_SELECTION_INVALID_SEMEN_SUPPLIER_HASHID,
                    'code': 'ERROR_ACCOUNT_SELECTION_INVALID_SEMEN_SUPPLIER_HASHID'
                }
            }
        
        semen_supplier_id = res[0]
    
    
    if feed_supplier_id == 0 and semen_supplier_id == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_SELECTION_NOTHING_SELECTED,
                'code': 'ERROR_ACCOUNT_SELECTION_NOTHING_SELECTED'
            }
        }
    
    
    data.user_id              = user_id
    data.feed_supplier_id     = feed_supplier_id
    data.semen_supplier_id    = semen_supplier_id
    
        
    res_add =  model['account_selection'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    
    cur_id      = res_add['account']['id']
    cur_hashid  = hashids_account.encrypt(cur_id)
    
    # remove plain id
    del res_add['account']['id']
    res_add['account']['hid'] = cur_hashid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)
    
        
    return res_add
    


def get_account_lookup_selection(account_id, sel_f_brand = 0, 
        sel_f_supplier = 0, sel_s_supplier = 0):
            
    res_f_brand = []
    if sel_f_brand > 0:
        res = model['account_selection'].get_business_obj_selection(account_id, 
            BUSINESS_OBJ_ID_FEED_BRAND)
    
        res_f_brand = [hashids_common.encrypt(cur_id) for cur_id in res] if res else []
    
    
    res_f_supplier = []
    if sel_f_supplier > 0:
        res = model['account_selection'].get_business_obj_selection(account_id, 
            BUSINESS_OBJ_ID_FEED_SUPPLIER)
    
        res_f_supplier = [hashids_common.encrypt(cur_id) for cur_id in res] if res else []
    
    res_s_supplier = []
    if sel_s_supplier > 0:
        res = model['account_selection'].get_business_obj_selection(account_id, 
            BUSINESS_OBJ_ID_SEMEN_SUPPLIER)
    
        res_s_supplier = [hashids_common.encrypt(cur_id) for cur_id in res] if res else []
    
    return {
        'f_brand':      res_f_brand,
        'f_supplier':   res_f_supplier,
        's_supplier':   res_s_supplier
    }
    
 
@app.get("/account/selection", tags=["Account"])
async def account_selection(request: Request, ahid: str, sel_f_brand: int = 0, 
        sel_f_supplier: int = 0, sel_s_supplier: int = 0):
    """
    Will get account_selection

    Parameters
    ----------
    ahid : str
        account hashid
    
    
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_SELECTION_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_SELECTION_INVALID_HASHID'
            }
        }
    
    
    account_id = res[0]
    
    
    res = get_account_lookup_selection(account_id, sel_f_brand, 
            sel_f_supplier, sel_s_supplier) 
    
    
    return {
            'result':{
                'num':  0,
                'code': 'SUCCESS'
            },
            
            'account_lookup': res
        }
    


@app.post("/account/selection/delete", tags=["Account"])
async def account_selection_delete(request: Request, data: dm.DataAccountSelection):
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
                'num':  ERROR_ACCOUNT_SELECTION_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_SELECTION_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    feed_brand_id       = None
    feed_supplier_id    = None 
    semen_supplier_id   = None
    
    feed_brand_hid = data.feed_brand_hid
    if feed_brand_hid is not None:
        res = hashids_common.decrypt(feed_brand_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_SELECTION_INVALID_FEED_BRAND_HASHID,
                    'code': 'ERROR_ACCOUNT_SELECTION_INVALID_FEED_BRAND_HASHID'
                }
            }
        
        feed_brand_id = res[0]
    
    
    feed_supplier_hid = data.feed_supplier_hid
    if feed_supplier_hid is not None:
        res = hashids_common.decrypt(feed_supplier_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_SELECTION_INVALID_FEED_SUPPLIER_HASHID,
                    'code': 'ERROR_ACCOUNT_SELECTION_INVALID_SUPPLIER_HASHID'
                }
            }
        
        feed_supplier_id = res[0]
    
    
    semen_supplier_hid = data.semen_supplier_hid
    if semen_supplier_hid is not None:
        res = hashids_common.decrypt(semen_supplier_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_SELECTION_INVALID_FEED_SUPPLIER_HASHID,
                    'code': 'ERROR_ACCOUNT_SELECTION_INVALID_SUPPLIER_HASHID'
                }
            }
        
        semen_supplier_id = res[0]
    
    
     
    data.user_id              = user_id
    data.feed_brand_id        = feed_brand_id    
    data.feed_supplier_id     = feed_supplier_id  
    data.semen_supplier_id    = semen_supplier_id
    
    res_delete = model['account_selection'].delete(data)
    
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    cur_id      = res_delete['account']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    # remove plain id
    del res_delete['account']['id']
    res_delete['account']['hid'] = cur_hid
        
    return res_delete
    
