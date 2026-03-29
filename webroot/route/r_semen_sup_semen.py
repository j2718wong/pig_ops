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


from r_a0_security_checks   import check_if_valid_user_account
from r_utils                import remove_database_null_description
    
    
@app.post("/semen_sup_semen/add", tags=["Common Lookup"])
async def semen_supplier_semen_add(request: Request, 
        data: dm.DataSemenSupplierSemen):
    
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
                'num':  ERROR_SEMEN_SUPPLIER_SEMEN_INVALID_NAME,
                'code': 'ERROR_SEMEN_SUPPLIER_SEMEN_INVALID_NAME'
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SUPPLIER_SEMEN_INVALID_USER_HASHID,
                'code': 'ERROR_SEMEN_SUPPLIER_SEMEN_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    semen_supplier_id   = 0
    semen_supplier_hid  = data.semen_supplier_hid
    
    res = hashids_common.decrypt(semen_supplier_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SUPPLIER_SEMEN_HASHID,
                'code': 'ERROR_SEMEN_SUPPLIER_SEMEN_HASHID'
            }
        }
    
    semen_supplier_id = res[0]
    
    
    data.name             = name
    data.user_id          = user_id
    data.semen_supplier_id = semen_supplier_id
    
    res_add    =  model['semen_sup_semen'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    cur_id    = res_add['semen_sup_semen']['id']
    cur_hid   = hashids_common.encrypt(cur_id)
    
    # remove plain id
    del res_add['semen_sup_semen']['id']
    res_add['semen_sup_semen']['hid'] = cur_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)
        
    return res_add
    

@app.post("/semen_sup_semen/update", tags=["Common Lookup"])
async def semen_supplier_semen_update(request: Request, 
        data: dm.DataSemenSupplierSemen):
    
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
                'num':  ERROR_SEMEN_SUPPLIER_SEMEN_INVALID_NAME,
                'code': 'ERROR_SEMEN_SUPPLIER_SEMEN_INVALID_NAME'
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SUPPLIER_SEMEN_INVALID_USER_HASHID,
                'code': 'ERROR_SEMEN_SUPPLIER_SEMEN_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    semen_supplier_id   = 0
    semen_supplier_hid  = data.semen_supplier_hid
    
    res = hashids_common.decrypt(semen_supplier_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SUPPLIER_SEMEN_HASHID,
                'code': 'ERROR_SEMEN_SUPPLIER_SEMEN_HASHID'
            }
        }
    
    semen_supplier_id = res[0]
    
    
    data.name      = name
    data.user_id   = user_id
    data.semen_supplier_id = semen_supplier_id
    
    res_update    =  model['semen_sup_semen'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    semen_supplier_id    = res_update['semen_supplier']['id']
    semen_supplier_hid   = hashids_common.encrypt(semen_supplier_id)
    
    # remove plain id
    del res_update['semen_supplier']['id']
    res_update['semen_supplier']['hid'] = semen_supplier_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
    
    
    return res_update
    


@app.get("/semen_sup_semen/list", tags=["Common Lookup"])
async def semen_supplier_semen_list(request: Request, semen_supplier_hid: str):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_common.decrypt(semen_supplier_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SUPPLIER_SEMEN_HASHID,
                'code': 'ERROR_SEMEN_SUPPLIER_SEMEN_HASHID'
            }
        }
    
    semen_supplier_id = res[0]
        
    res = model['semen_sup_semen'].get_list(semen_supplier_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
        
    
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }
    
    

    
