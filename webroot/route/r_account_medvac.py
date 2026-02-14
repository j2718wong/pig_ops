# January 14, 2026
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel
from fastapi.responses      import HTMLResponse
from fastapi                import Request

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



    
@app.post("/account_medvac/add", tags=["Account"])
async def account_medvac_add(account_medvac_data: dm.DataAccountMedVac):
    name    = account_medvac_data.name
    uhid    = account_medvac_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_MEDVAC_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_NAME'
            }
        }
        
       
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    medvac_brand_id     = 0
    medvac_brand_hid    = account_medvac_data.medvac_brand_hid
    
    if medvac_brand_hid is not None:
        res = hashids_common.decrypt(medvac_brand_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_MEDVAC_INVALID_MEDVAC_BRAND_HASHID,
                    'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_MEDVAC_BRAND_HASHID'
                }
            }
        
        medvac_brand_id = res[0]
    
    
    medvac_type_id     = 0
    medvac_type_hid    = account_medvac_data.medvac_type_hid
    
    if medvac_type_hid is not None:
        res = hashids_common.decrypt(medvac_type_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_MEDVAC_INVALID_MEDVAC_TYPE_HASHID,
                    'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_MEDVAC_TYPE_HASHID'
                }
            }
        
        medvac_type_id = res[0]
    
    
    
    
    account_medvac_data.name            = name
    account_medvac_data.user_id         = user_id
    account_medvac_data.medvac_brand_id = medvac_brand_id
    account_medvac_data.medvac_type_id  = medvac_type_id
    
    res_add    =  model['account_medvac'].add(account_medvac_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    account_medvac_id  = res_add['account_medvac']['id']
    account_medvac_hid = hashids_common.encrypt(account_medvac_id)
    
    # remove plain id
    del res_add['account_medvac']['id']
    res_add['account_medvac']['hid'] = account_medvac_hid


    # Remove optional desc coming from database
    remove_database_null_description(res_add)


    return res_add
    

@app.post("/account_medvac/update", tags=["Account"])
async def account_medvac_update(account_medvac_data: dm.DataAccountMedVac):
    name    = account_medvac_data.name
    uhid    = account_medvac_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_MEDVAC_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_NAME'
            }
        }
        
    
    operation_type  = account_medvac_data.operation_type
    
    if operation_type not in PIG_OPERATION_TYPES:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_MEDVAC_INVALID_OPERATION_TYPE,
                'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_OPERATION_TYPE'
            }
        }
        

    num_days_since = account_medvac_data.num_days_since
    
    if operation_type == PIG_OPERATION_TYPE_GESTATING:
        if num_days_since < 0 and num_days_since > 115:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_MEDVAC_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_NUMDAYS',
                    'desc': ''
                }
            }
            
    
    if operation_type == PIG_OPERATION_TYPE_LACTATING_PIGLETS:
        if num_days_since < 0 and num_days_since > 45:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_MEDVAC_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_NUMDAYS',
                    'desc': ''
                }
            }
    
    
    if operation_type == PIG_OPERATION_TYPE_GILT:
        if num_days_since < 0 and num_days_since > 300:
            return {
                'result':{
                    'num':  ERROR_ACCOUNT_MEDVAC_INVALID_NUMDAYS,
                    'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_NUMDAYS'
                }
            }
    
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    


    account_medvac_hid = account_medvac_data.account_medvac_hid
    res = hashids_common.decrypt(account_medvac_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_MEDVAC_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_HASHID'
            }
        }
    
    account_medvac_id = res[0]
    
    
    account_medvac_data.name      = name
    account_medvac_data.user_id   = user_id
    account_medvac_data.account_medvac_id = account_medvac_id
    
    res_update    =  model['account_medvac'].update(account_medvac_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['account_medvac']['id']
    res_update['account_medvac']['hid'] = account_medvac_hid
        
    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)

        
    return res_update
    

@app.get("/account_medvac/delete", tags=["Account"])
async def account_medvac_delete(uhid:str, ehid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_USER_HASHID'
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
                'num':  ERROR_ACCOUNT_MEDVAC_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_HASHID'
            }
        }
    
    account_medvac_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'account_medvac_id':   account_medvac_id
    }
    
    
    res_delete    =  model['account_medvac'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['account_medvac']['id']
    res_delete['account_medvac']['hid'] = ehid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_delete)

    
    return res_delete
    

@app.get("/account_medvac/list", tags=["Account"])
async def account_medvac_list(ahid: str,  inc_deleted: int = 0, 
        inc_user_audit:int = 0):
    """
    Will get account_medvac list.
    
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
                'num':  ERROR_ACCOUNT_MEDVAC_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_ACCOUNT_HASHID'
            }
        }
    
    
    account_id = res[0]
        
    res = model['account_medvac'].get_list(account_id, 
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
        cur_id  = cur_entry['acc_medvac']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['acc_medvac']['id']
        cur_entry['acc_medvac']['hid']   = cur_hid
        
            
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    
    
