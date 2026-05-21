# January 20, 2025
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


from fastapi.responses      import PlainTextResponse


import data_model           as dm


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)


from r_a0_security_checks   import check_if_valid_user_account
from r_utils                import remove_database_null_description

   
   
@app.post("/boar_ext_mate/add", tags=["Sow Boar"])
async def boar_external_mate_add(request: Request, data: dm.DataBoarExternalMate):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid        = data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_MATE_INVALID_USER_HASHID,
                'code': 'ERROR_SOW_BOAR_MATE_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    boar_hid       = data.boar_hid
    
    res = hashids_common.decrypt(boar_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_SOW_BOAR_MATE_INVALID_SOW_BOAR_HASHID,
                'code': 'ERROR_SOW_BOAR_MATE_INVALID_SOW_BOAR_HASHID'
            }
        }
    
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
    
        return result
    
    boar_id = res[0]
    
    
    boar_customer_hid       = data.boar_customer_hid
    
    res = hashids_common.decrypt(boar_customer_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_SOW_BOAR_MATE_INVALID_BOAR_CUSTOMER_HASHID,
                'code': 'ERROR_SOW_BOAR_MATE_INVALID_BOAR_CUSTOMER_HASHID'
            }
        }
    
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
    
        return result
    
    boar_customer_id = res[0]
    
    
    # Compute date_expected_birth and date_expected_payment
    
    dt_mate                 = datetime.strptime(data.date_mate, '%Y-%m-%d')
    dt_expected_birth       = dt_mate + timedelta(days=114)
    dt_expected_payment     = dt_mate + timedelta(days=156) # birth + 42 days
    
    dt_expected_birth_s     = datetime.strftime(dt_expected_birth, '%Y-%m-%d')
    dt_expected_payment_s   = datetime.strftime(dt_expected_payment, '%Y-%m-%d')
    
    
    data.user_id            = user_id
    data.boar_id            = boar_id
    data.boar_customer_id   = boar_customer_id
    data.date_expected_birth    = dt_expected_birth_s
    data.date_expected_payment  = dt_expected_payment_s
    
    
    res_add    =  model['sow_boar_mate'].add_boar_external_mate(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    sow_boar_mate_id     = res_add['sow_boar_mate']['id']
    sow_boar_mate_hid    = hashids_common.encrypt(sow_boar_mate_id)
    
    del res_add['sow_boar_mate']['id']
    res_add['sow_boar_mate']['hid'] = sow_boar_mate_hid
    
    
    # Add new_bill_hid
    if new_bill_hid is not None:
        res_add['result']['new_bill_hid'] = new_bill_hid
        
        
    # Remove optional desc coming from database
    remove_database_null_description(res_add)
        
    return res_add
    

@app.post("/boar_ext_mate/update", tags=["Sow Boar"])
async def boar_external_mate_update(request: Request, data: dm.DataBoarExternalMate):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid        = data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)
    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    sow_boar_mate_hid    = data.sow_boar_mate_hid
    res = hashids_common.decrypt(sow_boar_mate_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_MATE_INVALID_HASHID,
                'code': 'ERROR_SOW_BOAR_MATE_INVALID_HASHID'
            }
        }
    
    sow_boar_mate_id = res[0]
    
    
    
    
    data.user_id          = user_id
    data.sow_boar_mate_id = sow_boar_mate_id
    
    
    
    res_update  =  model['sow_boar_mate'].update_boar_external_mate(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
    
    # remove plain id
    clean_sow_boar_mate_entry(res_update)
    
    
    # Add new_bill_hid
    if new_bill_hid is not None:
        res_update['result']['new_bill_hid'] = new_bill_hid
        
        
    # Remove optional desc coming from database
    remove_database_null_description(res_update)
    
    
    return res_update
    

def get_data_sow_boar_mate_list(sow_boar_id, is_external = 0, pig_farm_id = 0):
    res = model['sow_boar_mate'].get_list(sow_boar_id, is_external, pig_farm_id)
    
    
    if res is None:
        return None
        
    
    if is_external == 0:
        # Replace plain id
        for cur_entry in res:
            
            cur_id     = cur_entry['id']
            cur_hid    = hashids_common.encrypt(cur_id)
            
            del cur_entry['id']
            cur_entry['hid'] = cur_hid
            


            cur_id     = cur_entry['pig_prod_id']
            cur_hid    = hashids_common.encrypt(cur_id)
            
            del cur_entry['pig_prod_id']
            cur_entry['pig_prod_hid'] = cur_hid
            
            
            
            cur_id     = cur_entry['mate_sow_boar']['id']
            cur_hid    = hashids_common.encrypt(cur_id)
            
            del cur_entry['mate_sow_boar']['id']
            cur_entry['mate_sow_boar']['hid'] = cur_hid
            
    else:
        # Replace plain id
        for cur_entry in res:
            cur_id     = cur_entry['id']
            cur_hid    = hashids_common.encrypt(cur_id)
            
            del cur_entry['id']
            cur_entry['hid'] = cur_hid

        
            cur_id     = cur_entry['boar_customer']['id']
            cur_hid    = hashids_common.encrypt(cur_id)
               
            del cur_entry['boar_customer']['id']
            cur_entry['boar_customer']['hid'] = cur_hid
            
            
            if 'sow_boar' in cur_entry:
            
                cur_id     = cur_entry['sow_boar']['id']
                cur_hid    = hashids_common.encrypt(cur_id)
                
                del cur_entry['sow_boar']['id']
                cur_entry['sow_boar']['hid'] = cur_hid
                
            

    return res


@app.get("/sow_boar_mate/list", tags=["Sow Boar"])
async def sow_boar_mate_list(request: Request, sow_boar_hid:str = None, 
        is_external:int = 0, pfhid: str = None):
    """
    Will get sow boar list.
    
    Parameters
    ----------
    sow_boar_hid:str
        sow_boar_hid; 
    
    
    is_external:
        only applicable if sow_boar_hid is a boar
        if > 0, will get external mates only
        if == 0, will get farm owned sows mated by the boar

    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    sow_boar_id = 0
    pig_farm_id = 0
    
    
    if sow_boar_hid is not None:
        res = hashids_common.decrypt(sow_boar_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SOW_BOAR_MATE_INVALID_SOW_BOAR_HASHID,
                    'code': 'ERROR_SOW_BOAR_MATE_INVALID_SOW_BOAR_HASHID'
                }
            }
        
        sow_boar_id = res[0]
        
    
    if pfhid is not None:
        res = hashids_common.decrypt(pfhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SOW_BOAR_MATE_INVALID_PIG_FARM_HASHID,
                    'code': 'ERROR_SOW_BOAR_MATE_INVALID_PIG_FARM_HASHID'
                }
            }
        
        pig_farm_id = res[0]
        
    
    res = get_data_sow_boar_mate_list(sow_boar_id, is_external, pig_farm_id)
            
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    
    # Get pig_farm.boar_ext_mate data_ver_num 
    pig_farm_ver_num = model['pig_farm'].get_data_ver_num(pig_farm_id)
    
    data_ver_num = {
        'pig_farm':{
            'boar_ext_mate': pig_farm_ver_num['data_ver_num']['boar_ext_mate']
        }
    }
    
        
    return {
        'result':{
            'num':  0
        },
        
        'data': res,
        
        'data_ver_num': data_ver_num
    }
    

