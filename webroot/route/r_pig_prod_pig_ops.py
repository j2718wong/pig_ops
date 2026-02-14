# August 29, 2025
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



@app.post("/pig_prod_pig_ops/update", tags=["Production Details"])
async def pig_prod_pig_ops_update(pig_prod_pig_ops_data: dm.DataPigProdPigOps):
    uhid    = pig_prod_pig_ops_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_PIG_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_PIG_OPS_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    pig_prod_pig_ops_hid = pig_prod_pig_ops_data.pig_prod_pig_ops_hid
    
    res = hashids_common.decrypt(pig_prod_pig_ops_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_PIG_OPS_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_PIG_OPS_INVALID_HASHID'
            }
        }
    
    
    pig_prod_pig_ops_id = res[0]
    
    
    staff_hid = pig_prod_pig_ops_data.staff_hid
    staff_id  = None
    
    # Needs staff info if not done_by_user
    if pig_prod_pig_ops_data.done_by_user == 0:
        res = hashids_common.decrypt(staff_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_PIG_OPS_INVALID_STAFF_HASHID,
                    'code': 'ERROR_PIG_PROD_PIG_OPS_INVALID_STAFF_HASHID'
                }
            }
        
        staff_id = res[0]
        
    
    
    
    pig_prod_pig_ops_data.user_id               = user_id
    pig_prod_pig_ops_data.pig_prod_pig_ops_id   = pig_prod_pig_ops_id
    pig_prod_pig_ops_data.staff_id              = staff_id
    
    res_update    =  model['pig_prod_pig_ops'].update(pig_prod_pig_ops_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['pig_prod_pig_ops']['id']
    res_update['pig_prod_pig_ops']['hid'] = pig_prod_pig_ops_hid
        
        
    if 'added_new_staff' in res_update:
        # Get new staff list fo refresh client staff_list
        
        pig_farm_id = res_update['pig_farm_id']
        del res_update['pig_farm_id']
        del res_update['added_new_staff']
        list_staff = model['pig_farm_staff'].get_list(pig_farm_id, minimum_info = 1)
        
        if list_staff is not None:
            for cur_entry in list_staff:
                cur_id      = cur_entry['pig_farm_staff']['id']
                cur_hid     = hashids_common.encrypt(cur_id)
            
                del cur_entry['pig_farm_staff']['id']
                cur_entry['pig_farm_staff']['hid']   = cur_hid
            
            res_update['staff_list'] = list_staff
            
            
    # Remove optional desc coming from database
    remove_database_null_description(res_update)

        
    return res_update
    

@app.post("/pig_prod_pig_ops/update_medvac", tags=["Production Details"])
async def pig_prod_pig_ops_update_medvac(pig_prod_pig_ops_data: dm.DataPigProdPigOps):
    uhid    = pig_prod_pig_ops_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_PIG_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_PIG_OPS_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    pig_prod_pig_ops_hid = pig_prod_pig_ops_data.pig_prod_pig_ops_hid
    
    res = hashids_common.decrypt(pig_prod_pig_ops_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_PIG_OPS_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_PIG_OPS_INVALID_HASHID'
            }
        }
    
    
    pig_prod_pig_ops_id = res[0]
    
    
    staff_hid = pig_prod_pig_ops_data.staff_hid
    staff_id  = None
    
    # Needs staff info if not done_by_user
    if pig_prod_pig_ops_data.done_by_user == 0:
        res = hashids_common.decrypt(staff_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_PIG_OPS_INVALID_STAFF_HASHID,
                    'code': 'ERROR_PIG_PROD_PIG_OPS_INVALID_STAFF_HASHID'
                }
            }
        
        staff_id = res[0]
        
    
    
    medvac_brand_hid = pig_prod_pig_ops_data.medvac_brand_hid
    
    res = hashids_common.decrypt(medvac_brand_hid)
    if len(res) == 0:
        result = {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_MEDVAC_BRAND_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_MEDVAC_BRAND_HASHID'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
        
        return result
        
    medvac_brand_id = res[0]
    

    
    medvac_type_hid = pig_prod_pig_ops_data.medvac_type_hid
    
    res = hashids_common.decrypt(medvac_type_hid)
    if len(res) == 0:
        result = {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_MEDVAC_TYPE_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_MEDVAC_TYPE_HASHID'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
        
        return result
    
    medvac_type_id = res[0]
    
    
    acc_medvac_hid = pig_prod_pig_ops_data.acc_medvac_hid
    
    res = hashids_common.decrypt(acc_medvac_hid)
    if len(res) == 0:
        result = {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_ACC_MEDVAC_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_ACC_MEDVAC_HASHID'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
        
        return result
    
    acc_medvac_id = res[0]
    
    
        
    
    pig_prod_pig_ops_data.user_id               = user_id
    pig_prod_pig_ops_data.pig_prod_pig_ops_id   = pig_prod_pig_ops_id
    pig_prod_pig_ops_data.staff_id              = staff_id
    
    pig_prod_pig_ops_data.medvac_brand_id       = medvac_brand_id
    pig_prod_pig_ops_data.medvac_type_id        = medvac_type_id
    pig_prod_pig_ops_data.acc_medvac_id         = acc_medvac_id
    
    
    
    res_update    =  model['pig_prod_pig_ops'].update_with_medvac(pig_prod_pig_ops_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['pig_prod_pig_ops']['id']
    res_update['pig_prod_pig_ops']['hid'] = pig_prod_pig_ops_hid
        
        
    if 'added_new_staff' in res_update:
        # Get new staff list fo refresh client staff_list
        
        pig_farm_id = res_update['pig_farm_id']
        del res_update['pig_farm_id']
        del res_update['added_new_staff']
        list_staff = model['pig_farm_staff'].get_list(pig_farm_id, minimum_info = 1)
        
        if list_staff is not None:
            for cur_entry in list_staff:
                cur_id      = cur_entry['pig_farm_staff']['id']
                cur_hid     = hashids_common.encrypt(cur_id)
            
                del cur_entry['pig_farm_staff']['id']
                cur_entry['pig_farm_staff']['hid']   = cur_hid
            
            res_update['staff_list'] = list_staff
            
    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
    
    return res_update
    


def replace_plain_ids_pig_prod_pig_ops(prod_pig_ops):
    for cur_entry in prod_pig_ops:
        cur_id  = cur_entry['pig_prod_pig_ops']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_prod_pig_ops']['id']
        cur_entry['pig_prod_pig_ops']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['account_pig_ops']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['account_pig_ops']['id']
        cur_entry['account_pig_ops']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['staff']['id']
        if cur_id is not None:
            cur_hid = hashids_common.encrypt(cur_id)
        else:
            cur_hid = None
        
        del cur_entry['staff']['id']
        cur_entry['staff']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['notes']['id']
        if cur_id is not None:
            cur_hid = hashids_common.encrypt(cur_id)
        else:
            cur_hid = None
        
        del cur_entry['notes']['id']
        cur_entry['notes']['hid']   = cur_hid
        
        
        if 'pig_medvac' in cur_entry:

            pig_medvac = cur_entry['pig_medvac']

            cur_id  = pig_medvac['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['pig_medvac']['id']
            cur_entry['pig_medvac']['hid'] = cur_hid
        
        
            cur_id  = pig_medvac['brand']['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['pig_medvac']['brand']['id']
            cur_entry['pig_medvac']['brand']['hid'] = cur_hid
        
            
            cur_id  = pig_medvac['type']['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['pig_medvac']['type']['id']
            cur_entry['pig_medvac']['type']['hid'] = cur_hid
        
        
            cur_id  = pig_medvac['acc_medvac']['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['pig_medvac']['acc_medvac']['id']
            cur_entry['pig_medvac']['acc_medvac']['hid'] = cur_hid
        
    


@app.get("/pig_prod_pig_ops/list", tags=["Production Details"])
async def pig_prod_pig_ops_list(prod_hid: str, operation_type: int):
    """
    Will get pig_prod_pig_ops list.
    
    Parameters
    ----------
    
    prod_hid:str
        pig_production hashid

    operation_type :int
        PIG_OPERATION_TYPE_GESTATING                        = 1
        PIG_OPERATION_TYPE_LACTATING_PIGLETS                = 2
        PIG_OPERATION_TYPE_LACTATING_SOW                    = 3
        PIG_OPERATION_TYPE_GILT                             = 4
        
         
        # Special operation type; This is not saved in database
        PIG_OPERATION_TYPE_LACTATING_COMBINED               = 10
        
        
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    
    
    res = hashids_common.decrypt(prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_PIG_OPS_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_PIG_PROD_PIG_OPS_INVALID_PIG_PROD_HASHID'
            }
        }
    
    
    pig_prod_id = res[0]
        
    res = model['pig_prod_pig_ops'].get_list(operation_type, 
        pig_prod_id = pig_prod_id, inc_user_audit = 1, order_by = 1)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # Replace plain id
    replace_plain_ids_pig_prod_pig_ops(res)


    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    

@app.get("/pig_prod_pig_ops/entry/{entry_hid}", tags=["Production Details"])
async def pig_prod_pig_ops_entry(entry_hid: str):
    """
    Will get pig_prod_pig_ops entry.
    
    Parameters
    ----------
    
    entry_hid:str
        pig_prod_pig_ops hashid

    
    """
    
    
    res = hashids_common.decrypt(entry_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_PIG_OPS_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_PIG_OPS_INVALID_HASHID'
            }
        }
    
    
    pig_prod_pig_ops_id = res[0]
        
    res = model['pig_prod_pig_ops'].get_entry(pig_prod_pig_ops_id, inc_user_audit = 1)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # Replace plain id
    replace_plain_ids_pig_prod_pig_ops(res)


    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res[0]
    }
    

    
