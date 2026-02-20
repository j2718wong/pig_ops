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


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)


from r_a0_security_checks   import check_if_valid_user_account
from r_utils                import remove_database_null_description



    
@app.post("/account_pig_buyer/add", tags=["Account"])
async def account_pig_buyer_add(account_pig_buyer_data: dm.DataAccountPigBuyer):
    name    = account_pig_buyer_data.name
    uhid    = account_pig_buyer_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_NAME'
            }
        }
        

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    
    level_1_id  = 0
    level_2_id  = 0
    level_3_id  = 0
    
    
    level_1_hid = account_pig_buyer_data.level_1_hid
    
    if level_1_hid is not None:
        res = hashids_common.decrypt(level_1_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACC_PIG_BUYER_INVALID_ADDRESS_LEVEL_1,
                    'code': 'ERROR_ACC_PIG_BUYER_INVALID_ADDRESS_LEVEL_1'
                }
            }
            
        level_1_id = res[0]
    
    
    level_2_hid = account_pig_buyer_data.level_2_hid
    
    if level_2_hid is not None:
        res = hashids_common.decrypt(level_2_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACC_PIG_BUYER_INVALID_ADDRESS_LEVEL_2,
                    'code': 'ERROR_ACC_PIG_BUYER_INVALID_ADDRESS_LEVEL_2'
                }
            }
        
        level_2_id = res[0]
    
    
    level_3_hid = account_pig_buyer_data.level_3_hid
    
    if level_3_hid is not None:
        res = hashids_common.decrypt(level_3_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ACC_PIG_BUYER_INVALID_ADDRESS_LEVEL_3,
                    'code': 'ERROR_ACC_PIG_BUYER_INVALID_ADDRESS_LEVEL_3'
                }
            }
        
        level_3_id = res[0]
    

    
    account_pig_buyer_data.name         = name
    account_pig_buyer_data.user_id      = user_id
    account_pig_buyer_data.level_1_id   = level_1_id
    account_pig_buyer_data.level_2_id   = level_2_id
    account_pig_buyer_data.level_3_id   = level_3_id
    
    
    res_add    =  model['account_pig_buyer'].add(account_pig_buyer_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    account_pig_buyer_id  = res_add['account_pig_buyer']['id']
    account_pig_buyer_hid = hashids_common.encrypt(account_pig_buyer_id)
    
    # remove plain id
    del res_add['account_pig_buyer']['id']
    res_add['account_pig_buyer']['hid'] = account_pig_buyer_hid


    # Remove optional desc coming from database
    remove_database_null_description(res_add)


    return res_add
    

@app.post("/account_pig_buyer/update", tags=["Account"])
async def account_pig_buyer_update(account_pig_buyer_data: dm.DataAccountPigBuyer):
    name    = account_pig_buyer_data.name
    uhid    = account_pig_buyer_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_NAME'
            }
        }
        
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    account_pig_buyer_hid = account_pig_buyer_data.account_pig_buyer_hid
    res = hashids_common.decrypt(account_pig_buyer_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_HASHID'
            }
        }
    
    account_pig_buyer_id = res[0]
    
    
    account_pig_buyer_data.name      = name
    account_pig_buyer_data.user_id   = user_id
    account_pig_buyer_data.account_pig_buyer_id = account_pig_buyer_id
    
    res_update    =  model['account_pig_buyer'].update(account_pig_buyer_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['account_pig_buyer']['id']
    res_update['account_pig_buyer']['hid'] = account_pig_buyer_hid
        
    return res_update
    

@app.get("/account_pig_buyer/delete", tags=["Account"])
async def account_pig_buyer_delete(uhid:str, ehid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_USER_HASHID'
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
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_HASHID'
            }
        }
    
    account_pig_buyer_id = res[0]
    
    
    data = {
        'user_id':              user_id,
        'account_pig_buyer_id':   account_pig_buyer_id
    }
    
    
    res_delete    =  model['account_pig_buyer'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['account_pig_buyer']['id']
    res_delete['account_pig_buyer']['hid'] = ehid
        
    return res_delete
    

@app.get("/account_pig_buyer/list", tags=["Account"])
async def account_pig_buyer_list(ahid: str, inc_deleted: int = 0, 
        inc_user_audit:int = 0):
    """
    Will get account_pig_buyer list.
    
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
                'num':  ERROR_ACCOUNT_PIG_BUYER_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_ACCOUNT_PIG_BUYER_INVALID_ACCOUNT_HASHID'
            }
        }
    
    
    account_id = res[0]
        
    res = model['account_pig_buyer'].get_list(account_id, inc_deleted, inc_user_audit)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
            
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['pig_buyer']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_buyer']['id']
        cur_entry['pig_buyer']['hid']   = cur_hid
        
            
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    
    
