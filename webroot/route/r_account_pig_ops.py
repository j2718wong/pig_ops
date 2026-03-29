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


@app.get("/acc_pig_ops", response_class = HTMLResponse, tags=["Account"])
async def account_pig_ops(request: Request, ahid:str = None):
    # Get the current logged in user;
    
    
    account_id = 1
    
    if ahid is not None:
        res = hashids_account.decrypt(ahid)
        if len(res) == 0:
            # Just proceed if it is invalid; will get default 
            # account hid from user if not given
            account_id = 1
            
            """
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID'
                }
            }
            """
        else:
            account_id = res[0]
            
    
    # Get account info
    data_account = model['account'].get_info(account_id)
    if data_account == None:
        # TODO what to do in case no result
        return None
        
        
    # TODO Check account free trial period
        
    # TODO check account for not paid bill
    
        
    # Get all account pig ops order by operation_type ASC, num_days ASC
    acc_pig_ops = model['account_pig_ops'].get_list(account_id, None, 
            inc_user_audit = 1)
    
    
    # Remove not useful blocks
    del data_account['account']
    del data_account['farm_ids']
    
    if data_account['settings_operations']['last_update']['name_last'] is None:
        del data_account['settings_operations']['last_update']
    
    
    # Replace plain_ids
    for cur_entry in acc_pig_ops:
        cur_id      = cur_entry['acc_pig_ops']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['acc_pig_ops']['id']
        cur_entry['acc_pig_ops']['hid']   = cur_hid
        
        # Remove not useful blocks
        if cur_entry['last_update']['name_last'] is None:
            del cur_entry['last_update']
    
    
    page_data = {
        'account':                  data_account,
        'acc_pig_ops':              acc_pig_ops,
    }
    

    page = controller.view['acc_pig_ops'].render(page_data = json.dumps(page_data, indent=4))
    
    return page


    
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
        1 = GESTATING; 2 = LACTATING_PIGLETS; 3 = LACTATING_SOW; 4 = GILTS
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
        
            
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }
    
    
