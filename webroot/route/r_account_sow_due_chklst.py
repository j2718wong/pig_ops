# May 20, 2026
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



    
@app.post("/acc_sow_due_chklst/add", tags=["Account"])
async def acc_sow_due_chklst_add(request: Request, data: dm.DataAccountChecklist):
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
    
    res_add    =  model['acc_sow_due_chklst'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    cur_id  = res_add['account_checklist']['id']
    cur_hid = hashids_common.encrypt(cur_id)
    
    # remove plain id
    del res_add['account_checklist']['id']
    res_add['account_checklist']['hid'] = cur_hid


    # Remove optional desc coming from database
    remove_database_null_description(res_add)

    return res_add
    

@app.post("/acc_sow_due_chklst/update", tags=["Account"])
async def acc_sow_due_chklst_update(request: Request, data: dm.DataAccountPigOps):
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
    
    
    
    acc_sow_due_chklst_hid = data.acc_sow_due_chklst_hid
    res = hashids_common.decrypt(acc_sow_due_chklst_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_OPS_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_OPS_INVALID_HASHID'
            }
        }
    
    acc_sow_due_chklst_id = res[0]
    
    
    data.name      = name
    data.user_id   = user_id
    data.acc_sow_due_chklst_id = acc_sow_due_chklst_id
    
    res_update    =  model['acc_sow_due_chklst'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['acc_sow_due_chklst']['id']
    res_update['acc_sow_due_chklst']['hid'] = acc_sow_due_chklst_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
    
    return res_update
    

@app.get("/acc_sow_due_chklst/delete", tags=["Account"])
async def acc_sow_due_chklst_delete(request: Request, ehid: str):
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
    
    acc_sow_due_chklst_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'acc_sow_due_chklst_id':   acc_sow_due_chklst_id
    }
    
    
    res_delete    =  model['acc_sow_due_chklst'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['acc_sow_due_chklst']['id']
    res_delete['acc_sow_due_chklst']['hid'] = ehid
        
    return res_delete
    

@app.get("/acc_sow_due_chklst", tags=["Account"])
async def acc_sow_due_chklst_list(request: Request, ahid: str,  
        inc_deleted: int = 0, inc_user_audit:int = 0):
    """
    Will get acc_sow_due_chklst list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid
        
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
        
    res = model['acc_sow_due_chklst'].get_list(account_id,
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
        cur_id  = cur_entry['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
        
    
    # Get account.sow_due_checklist data_ver_num 
    account_ver_num = model['account'].get_data_ver_num(account_id)
    
    data_ver_num = {
        'account':{
            'sow_due_checklist': account_ver_num['data_ver_num']['sow_due_checklist']
        }
    }

            
    return {
        'result':{
            'num':  0
        },
        
        'data': res,
        
        'account_ver_num': account_ver_num
    }
    
    
