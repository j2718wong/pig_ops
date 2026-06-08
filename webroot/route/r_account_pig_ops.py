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


PIG_OPERATION_TYPES = [
    PIG_OPERATION_TYPE_GESTATING,
    PIG_OPERATION_TYPE_LACTATING_PIGLETS,
    PIG_OPERATION_TYPE_LACTATING_SOW,
    PIG_OPERATION_TYPE_GILT,
    PIG_OPERATION_TYPE_WEANING_SOW
]


    
@app.post("/account_pig_ops/add", tags=["Account"])
async def account_pig_ops_add(request: Request, data: dm.DataAccountPigOps):
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
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    operation_type  = data.operation_type
    
    if operation_type not in PIG_OPERATION_TYPES:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_OPERATION_TYPE,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_OPERATION_TYPE'
            }
        }
        

    num_days_since = data.num_days_since
    
    if operation_type == PIG_OPERATION_TYPE_GESTATING:
        if num_days_since < 0 and num_days_since > 115:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS'
                }
            }
            
    
    if operation_type == PIG_OPERATION_TYPE_LACTATING_PIGLETS:
        if num_days_since < 0 and num_days_since > 45:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS'
                }
            }
    
    
    if operation_type == PIG_OPERATION_TYPE_GILT:
        if num_days_since < 0 and num_days_since > 300:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS'
                }
            }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    data.name      = name
    data.user_id   = user_id
    
    res_add    =  model['account_pig_ops'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    account_pig_ops_id  = res_add['account_pig_ops']['id']
    account_pig_ops_hid = hashids_common.encrypt(account_pig_ops_id)
    
    # remove plain id
    del res_add['account_pig_ops']['id']
    res_add['account_pig_ops']['hid'] = account_pig_ops_hid


    # Remove optional desc coming from database
    remove_database_null_description(res_add)

    return res_add
    

@app.post("/account_pig_ops/update", tags=["Account"])
async def account_pig_ops_update(request: Request, data: dm.DataAccountPigOps):
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
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NAME'
            }
        }
        
    
    operation_type  = data.operation_type
    
    if operation_type not in PIG_OPERATION_TYPES:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_OPERATION_TYPE,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_OPERATION_TYPE'
            }
        }
        

    num_days_since = data.num_days_since
    
    if operation_type == PIG_OPERATION_TYPE_GESTATING:
        if num_days_since < 0 and num_days_since > 115:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS',
                    'desc': ''
                }
            }
            
    
    if operation_type == PIG_OPERATION_TYPE_LACTATING_PIGLETS:
        if num_days_since < 0 and num_days_since > 45:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS',
                    'desc': ''
                }
            }
    
    
    if operation_type == PIG_OPERATION_TYPE_GILT:
        if num_days_since < 0 and num_days_since > 300:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_NUMDAYS'
                }
            }
    
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    account_pig_ops_hid = data.account_pig_ops_hid
    res = hashids_common.decrypt(account_pig_ops_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_HASHID'
            }
        }
    
    account_pig_ops_id = res[0]
    
    
    data.name      = name
    data.user_id   = user_id
    data.account_pig_ops_id = account_pig_ops_id
    
    res_update    =  model['account_pig_ops'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['account_pig_ops']['id']
    res_update['account_pig_ops']['hid'] = account_pig_ops_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
    
    return res_update
    

@app.get("/account_pig_ops/delete", tags=["Account"])
async def account_pig_ops_delete(request: Request, ehid: str):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    res = hashids_common.decrypt(ehid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_HASHID'
            }
        }
    
    account_pig_ops_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'account_pig_ops_id':   account_pig_ops_id
    }
    
    
    res_delete    =  model['account_pig_ops'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['account_pig_ops']['id']
    res_delete['account_pig_ops']['hid'] = ehid
        
    return res_delete
    

@app.get("/account_pig_ops/list", tags=["Account"])
async def account_pig_ops_list(request: Request, ahid: str, operation_type: int = None, 
        inc_deleted: int = 0, inc_user_audit:int = 0):
    """
    Will get account_pig_ops list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid
        
    operation_type :int
        1 = GESTATING; 
        2 = LACTATING_PIGLETS; 
        3 = LACTATING_SOW; 
        4 = GILTS
        5 = WEANING_SOWS 
        
        if None, will get all.
    
    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
        
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
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_ACCOUNT_HASHID'
            }
        }
    
    
    account_id = res[0]
        
    res = model['account_pig_ops'].get_list(account_id, operation_type,
            inc_deleted, inc_user_audit)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
            
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['acc_pig_ops']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['acc_pig_ops']['id']
        cur_entry['acc_pig_ops']['hid']   = cur_hid
        
        
    # Get account data_ver_num
    res_ver_num     = model['account'].get_data_ver_num(account_id)
    account_ver_num = res_ver_num['data_ver_num']
    
    
    data_ver_num    = None
    
    if operation_type is None:
        data_ver_num = {
            'account':{
                'gestating_ops':        account_ver_num['gesta_ops'],
                'lactating_piglets_ops':account_ver_num['lacta_piglets_ops'],
                'lactating_sow_ops':    account_ver_num['lacta_sow_ops'],
                'gilt_ops':             account_ver_num['gilt_ops'],
                'weaning_sow_ops':      account_ver_num['weaning_sow_ops']
            }
        }
    
    else:
        if operation_type == PIG_OPERATION_TYPE_GESTATING:
            data_ver_num = {
                'account':{
                    'gestating_ops':    account_ver_num['gesta_ops']
                }
            }
        
        if operation_type == PIG_OPERATION_TYPE_LACTATING_PIGLETS:
            data_ver_num = {
                'account':{
                    'lactating_piglets_ops':account_ver_num['lacta_piglets_ops']
                }
            }
        
        if operation_type == PIG_OPERATION_TYPE_LACTATING_SOW:
            data_ver_num = {
                'account':{
                    'lactating_sow_ops':    account_ver_num['lacta_sow_ops']
                }
            }

        if operation_type == PIG_OPERATION_TYPE_GILT:
            data_ver_num = {
                'account':{
                    'gilt_ops':         account_ver_num['gilt_ops']
                }
            }

        if operation_type == PIG_OPERATION_TYPE_WEANING_SOW:
            data_ver_num = {
                'account':{
                    'weaning_sow_ops':  account_ver_num['weaning_sow_ops']
                }
            }


    return {
        'result':{
            'num':  0
        },
        
        'data': res,
        
        'data_ver_num': data_ver_num
    }
    
    
