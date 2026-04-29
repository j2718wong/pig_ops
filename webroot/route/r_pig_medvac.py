# January 12, 2026
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

   
@app.post("/pig_medvac/add", tags=["Pig Details"])
async def pig_medvac_add(request: Request, data: dm.DataPigMedvac):
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
                'num':  ERROR_PIG_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    
    sow_boar_id         = 0
    pig_prod_id         = 0         
    pig_prod_pig_ops_id = 0
    health_issue_id     = 0
    
    medvac_brand_id     = 0
    medvac_type_id      = 0
    acc_medvac_id       = 0
    staff_id            = 0
    
    
    sow_boar_hid        = data.sow_boar_hid
    
    if sow_boar_hid is not None:
        res = hashids_common.decrypt(sow_boar_hid)
        if len(res) == 0:
            result =  {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_SOW_BOAR_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_SOW_BOAR_HASHID'
                }
            }
            
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
            
        sow_boar_id = res[0]
    
    
    
    pig_prod_hid        = data.pig_prod_hid
    
    if pig_prod_hid is not None:
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            result =  {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_PIG_PROD_HASHID'
                }
            }
            
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
            
            return result
            
        pig_prod_id = res[0]
    
    
    
    pig_prod_pig_ops_hid = data.pig_prod_pig_ops_hid
    
    if pig_prod_pig_ops_hid is not None:
        res = hashids_common.decrypt(pig_prod_pig_ops_hid)
        if len(res) == 0:
            result =  {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_PIG_PROD_PIG_OPS_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_PIG_PROD_PIG_OPS_HASHID'
                }
            }
            
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
            
            return result
        
        pig_prod_id = res[0]
    
    
    
    health_issue_hid        = data.health_issue_hid
    
    if health_issue_hid is not None:
        res = hashids_common.decrypt(health_issue_hid)
        if len(res) == 0:
            result = {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_HEALTH_ISSUE_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_HEALTH_ISSUE_HASHID'
                }
            }
            
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
            
            return result
        
        health_issue_id = res[0]
    
    
    

    staff_hid = data.staff_hid
    
    if staff_hid is not None:
        res = hashids_common.decrypt(staff_hid)
        if len(res) == 0:
            result = {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_STAFF_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_STAFF_HASHID'
                }
            }
            
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
            
            return result
            
        staff_id = res[0]
    
    
    medvac_brand_hid = data.medvac_brand_hid
    
    if medvac_brand_hid is not None:
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
        

    
    medvac_type_hid = data.medvac_type_hid
    
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
    
    
    acc_medvac_hid = data.acc_medvac_hid
    
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
    
    
    # Check for valid keys
    if sow_boar_id == 0 and pig_prod_id == 0 and pig_prod_pig_ops_id == 0 and health_issue_id == 0:
        result = {
            'result':{
                'num':  ERROR_PIG_MEDVAC_NO_VALID_KEY,
                'code': 'ERROR_PIG_MEDVAC_NO_VALID_KEY'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
        
        return result
        
        
   
    data.user_id            = user_id
    data.sow_boar_id        = sow_boar_id
    data.pig_prod_id        = pig_prod_id
    data.pig_prod_pig_ops_id = pig_prod_pig_ops_id
    data.health_issue_id    = health_issue_id
        
    data.medvac_brand_id    = medvac_brand_id
    data.medvac_type_id     = medvac_type_id
    data.acc_medvac_id      = acc_medvac_id  
    data.staff_id           = staff_id
    
    
    res_add    =  model['pig_medvac'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    cur_id    = res_add['pig_medvac']['id']
    cur_hid   = hashids_common.encrypt(cur_id)
    
    del res_add['pig_medvac']['id']
    res_add['pig_medvac']['hid'] = cur_hid

    
    # Add new_bill_hid
    if new_bill_hid is not None:
        res_add['result']['new_bill_hid'] = new_bill_hid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)

        
    return res_add
    

@app.post("/pig_medvac/update", tags=["Pig Details"])
async def pig_medvac_update(request: Request, data: dm.DataPigMedvac):
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
                'num':  ERROR_PIG_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    pig_medvac_id       = 0
    pig_medvac_hid      = data.pig_medvac_hid
    
    if pig_medvac_hid is not None:
        res = hashids_common.decrypt(pig_medvac_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_HASHID'
                }
            }
        
        pig_medvac_id = res[0]
    
    else:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_HASHID'
            }
        }
    
    
    staff_id            = 0
    medvac_brand_id     = 0
    medvac_type_id      = 0
    acc_medvac_id       = 0
    
    

    staff_hid = data.staff_hid
    
    if staff_hid is not None:
        res = hashids_common.decrypt(staff_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_STAFF_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_STAFF_HASHID'
                }
            }
        
        staff_id = res[0]
    
    
    medvac_brand_hid = data.medvac_brand_hid
    
    res = hashids_common.decrypt(medvac_brand_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_MEDVAC_BRAND_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_MEDVAC_BRAND_HASHID'
            }
        }
    
    medvac_brand_id = res[0]
    
    
    medvac_type_hid = data.medvac_type_hid
    
    res = hashids_common.decrypt(medvac_type_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_MEDVAC_TYPE_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_MEDVAC_TYPE_HASHID'
            }
        }
    
    medvac_type_id = res[0]
    
    
    acc_medvac_hid = data.acc_medvac_hid
    
    res = hashids_common.decrypt(acc_medvac_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_ACC_MEDVAC_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_INVALID_ACC_MEDVAC_HASHID'
            }
        }
    
    acc_medvac_id = res[0]
    
    
   
    data.user_id         = user_id
    data.pig_medvac_id   = pig_medvac_id
    
    data.medvac_brand_id = medvac_brand_id
    data.medvac_type_id  = medvac_type_id
    data.acc_medvac_id   = acc_medvac_id  
    data.staff_id        = staff_id
    
    
    res_update    =  model['pig_medvac'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)

    
    return res_update
    

@app.get("/pig_medvac/delete", tags=["Pig Details"])
async def pig_medvac_delete(request: Request, ehid: str):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(ehid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_HASHID'
            }
        }
    
    pig_race_line_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'pig_race_line_id':     pig_race_line_id
    }
    
    
    res_delete    =  model['pig_race_line'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['pig_race_line']['id']
    res_delete['pig_race_line']['hid'] = ehid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_delete)

    
    return res_delete
    
    
def get_data_pig_medvac(sow_boar_id, pig_prod_id, inc_deleted, inc_user_audit):
    res = model['pig_medvac'].get_list(sow_boar_id, pig_prod_id,
            inc_deleted, inc_user_audit)
    
    if res is None: 
        return None
    
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['medvac']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['medvac']['id']
        cur_entry['medvac']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['medvac']['health_issue_id']
        if cur_id is not None:
            cur_hid = hashids_common.encrypt(cur_id)
        
            del cur_entry['medvac']['health_issue_id']
            cur_entry['medvac']['health_issue_hid']   = cur_hid
        else:
            del cur_entry['medvac']['health_issue_id']
            
        
        cur_id  = cur_entry['medvac']['prod_pig_ops_id']
        if cur_id is not None:
            cur_hid = hashids_common.encrypt(cur_id)
        
            del cur_entry['medvac']['prod_pig_ops_id']
            cur_entry['medvac']['prod_pig_ops_hid']   = cur_hid
        else:
            del cur_entry['medvac']['prod_pig_ops_id']
        
        
        
        cur_id  = cur_entry['medvac']['brand']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['medvac']['brand']['id']
        cur_entry['medvac']['brand']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['medvac']['type']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['medvac']['type']['id']
        cur_entry['medvac']['type']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['medvac']['acc_medvac']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['medvac']['acc_medvac']['id']
        cur_entry['medvac']['acc_medvac']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['medvac']['staff']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['medvac']['staff']['id']
        cur_entry['medvac']['staff']['hid']   = cur_hid
    
    return res
    
    
@app.get("/pig_medvac/list", tags=["Pig Details"])
async def pig_medvac_list(request: Request, sow_boar_hid: str = None, 
        pig_prod_hid: str = None, inc_deleted: int = 0, inc_user_audit:int = 0):
    """
    Will get pig medvac list.
    
    Parameters
    ----------
    
    sow_boar_hid:str
        sow_boar hashid

    pig_prod_hid:str
        pig_prod hashid


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
    
    
    sow_boar_id = 0
    pig_prod_id = 0
    
    if sow_boar_hid is not None:
    
        res = hashids_common.decrypt(sow_boar_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_SOW_BOAR_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_SOW_BOAR_HASHID'
                }
            }
        
        
        sow_boar_id = res[0]
        
        
    if pig_prod_hid is not None:
    
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_PIG_PROD_HASHID'
                }
            }
        
        
        pig_prod_id = res[0]
    
    
    if sow_boar_id == 0 and pig_prod_id == 0:
        result = {
            'result':{
                'num':  ERROR_PIG_MEDVAC_NO_VALID_KEY,
                'code': 'ERROR_PIG_MEDVAC_NO_VALID_KEY'
            }
        }
        
        return result
        
        
    res = get_data_pig_medvac(sow_boar_id, pig_prod_id, inc_deleted, inc_user_audit)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }
    
    
@app.get("/pig_medvac/search_keys", tags=["Pig Details"])
async def pig_medvac_search_keys(request: Request, ahid: str, search_keyword: None):
    """
    Will return pig_medvac search keys from given pig_farm account hid and a keyword;.
    This is used in searching pig_medvac. Note this will search 
    all pig_medvac of the account not just for a specific sow_boar. 
    This is because this feature is much more useful if all sow_boar of the
    account is searched to know which pigs have taken a particular medvac.
    
    This is requested in every keyboard stroke in a search input, 
    so this has to execute as fast as possible.
    
    Parameters
    ----------
    
    ahid:str
        pig farm account hashid

    search_keyword: str
        keyword
    
    
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
                'num':  ERROR_PIG_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_USER_HASHID'
            }
        }
    
    account_id = res[0]
    
    
        
    res = model['pig_medvac'].get_search_keywords(account_id, search_keyword)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }
    
    

    
    
