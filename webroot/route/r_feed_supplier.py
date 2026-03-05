# August 24, 2025
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


from r_utils                import get_location_address_names_and_replace_ids


    
@app.post("/feed_supplier/add", tags=["Common Lookup"])
async def feed_supplier_add(request: Request, data: dm.DataFeedSupplier):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    name    = data.name
    #uhid    = data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_SUPPLIER_INVALID_NAME,
                'code': 'ERROR_FEED_SUPPLIER_INVALID_NAME',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_SUPPLIER_INVALID_USER_HASHID,
                'code': 'ERROR_FEED_SUPPLIER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    level_1_id  = 0
    level_2_id  = 0
    level_3_id  = 0
    
    
    level_1_hid = data.level_1_hid
    res = hashids_common.decrypt(level_1_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_SUPPLIER_INVALID_ADDRESS_LEVEL_1,
                'code': 'ERROR_FEED_SUPPLIER_INVALID_ADDRESS_LEVEL_1',
                'desc': ''
            }
        }
        
    level_1_id = res[0]
    
    
    level_2_hid = data.level_2_hid
    res = hashids_common.decrypt(level_2_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_SUPPLIER_INVALID_ADDRESS_LEVEL_2,
                'code': 'ERROR_FEED_SUPPLIER_INVALID_ADDRESS_LEVEL_2',
                'desc': ''
            }
        }
    
    level_2_id = res[0]
    
    
    level_3_hid = data.level_3_hid
    
    if level_3_hid is not None:
        res = hashids_common.decrypt(level_3_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_FEED_SUPPLIER_INVALID_ADDRESS_LEVEL_3,
                    'code': 'ERROR_FEED_SUPPLIER_INVALID_ADDRESS_LEVEL_3',
                    'desc': ''
                }
            }
        
        level_3_id = res[0]
    
    
    
    
    data.name         = name
    data.user_id      = user_id
    data.level_1_id   = level_1_id
    data.level_2_id   = level_2_id
    data.level_3_id   = level_3_id
    
    
    res_add    =  model['feed_supplier'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    #Replace Plain Id
    cur_id      = res_add['feed_supplier']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del res_add['feed_supplier']['id']
    res_add['feed_supplier']['hid']   = cur_hid
    
    
    get_location_address_names_and_replace_ids(res_add)
        
    
    return res_add
    

@app.post("/feed_supplier/update", tags=["Common Lookup"])
async def feed_supplier_update(request: Request, data: dm.DataFeedSupplier):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    name    = data.name
    #uhid    = data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_SUPPLIER_INVALID_NAME,
                'code': 'ERROR_FEED_SUPPLIER_INVALID_NAME',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_SUPPLIER_INVALID_USER_HASHID,
                'code': 'ERROR_FEED_SUPPLIER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    feed_supplier_hid = data.feed_supplier_hid
    
    res = hashids_common.decrypt(feed_supplier_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_SUPPLIER_HASHID,
                'code': 'ERROR_FEED_SUPPLIER_HASHID',
                'desc': ''
            }
        }
    
    feed_supplier_id = res[0]
    
    
    data.name      = name
    data.user_id   = user_id
    data.feed_supplier_id = feed_supplier_id
    
    res_update      =  model['feed_supplier'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    # remove plain id
    del res_update['feed_supplier']['id']
    res_update['feed_supplier']['hid'] = feed_supplier_hid

        
    return res_update
    

   
@app.get("/feed_supplier/list", tags=["Common Lookup"])
async def feed_supplier_list(request: Request, ahid:str = None, level_2_hid: str = None):
    """
    Will get feed_supplier list.
    
    Parameters
    ----------
    
    level_2_hid:str
        level_2_hid

    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    account_id      = 0
    adrs_level_2_id = 0
    
            
            
    if level_2_hid is not None:
            
        res = hashids_common.decrypt(level_2_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_ADDRESS_LEVEL_2_HID,
                    'code': 'ERROR_ADDRESS_LEVEL_2_HID',
                    'desc': ''
                }
            }
        
        adrs_level_2_id = res[0]
        
        
        res = model['feed_supplier'].get_list(
                address_level_2_id  = adrs_level_2_id,
                minimum_info        = 1)

        
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
            cur_id      = cur_entry['id']
            cur_hid     = hashids_common.encrypt(cur_id)
            
            del cur_entry['id']
            cur_entry['hid']   = cur_hid
                
                
            cur_id      = cur_entry['level_3_id']
            cur_hid     = hashids_common.encrypt(cur_id)
            
            del cur_entry['level_3_id']
            cur_entry['level_3_hid']   = cur_hid
            
            
                
        return {
            'result':{
                'num':  0,
                'code': 'SUCCESS',
                'desc': ''
            },
            
            'data': res
        }
            
        
    
    if ahid is not None:
        res = hashids_account.decrypt(ahid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_FEED_SUPPLIER_INVALID_ACCOUNT_HASHID,
                    'code': 'ERROR_FEED_SUPPLIER_INVALID_ACCOUNT_HASHID',
                    'desc': ''
                }
            }
        
        account_id = res[0]
        
        
        res = model['feed_supplier'].get_list(account_id = account_id, 
                minimum_info = 0)

        
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
                get_location_address_names_and_replace_ids(cur_entry)
                    
                    
            return {
                'result':{
                    'num':  0,
                    'code': 'SUCCESS',
                    'desc': ''
                },
                
                'data': res
            }
            
            

    
