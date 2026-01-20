# January 20, 2025
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel
from fastapi.responses      import HTMLResponse

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

   
   
@app.post("/sow_boar_mate/add", tags=["Sow Boar"])
async def sow_boar_mate_add(sow_boar_mate_data: dm.DataSowBoarMate):
    uhid        = sow_boar_mate_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_MATE_INVALID_USER_HASHID,
                'code': 'ERROR_SOW_BOAR_MATE_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    pfhid       = sow_boar_mate_data.pfhid
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_SOW_BOAR_MATE_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_SOW_BOAR_MATE_INVALID_PIG_FARM_HASHID'
            }
        }
    
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
    
        return result
    
    pig_farm_id = res[0]
    
    
    number  = None
    name    = None
    
    sow_boar_mate_number     = sow_boar_mate_data.number
    if sow_boar_mate_number is not None:
        number      = sow_boar_mate_number.strip()
       
            
            
    sow_boar_mate_name       = sow_boar_mate_data.name
    if sow_boar_mate_name is not None:
        name        = sow_boar_mate_name.strip()
        
    
    if name is None and number is None:
        result = {
            'result':{
                'num':  ERROR_SOW_BOAR_MATE_NO_SOW_BOAR_NUMBER_OR_NAME,
                'code': 'ERROR_SOW_BOAR_MATE_NO_SOW_BOAR_NUMBER_OR_NAME'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
    
        return result
    
    
    parent_sow_id       = 0
    parent_sow_hid      = sow_boar_mate_data.parent_sow_hid
    
    if parent_sow_hid is not None:
        res = hashids_common.decrypt(parent_sow_hid)
        
        if len(res) == 0:
            result =  {
                'result':{
                    'num':  ERROR_SOW_BOAR_MATE_INVALID_PARENT_SOW_HASHID,
                    'code': 'ERROR_SOW_BOAR_MATE_INVALID_PARENT_SOW_HASHID'
                }
            }
        
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
        
            return result
        
        parent_sow_id = res[0]
        
    
    parent_boar_id      = 0
    parent_boar_hid     = sow_boar_mate_data.parent_boar_hid
    
    if parent_boar_hid is not None:
        res = hashids_common.decrypt(parent_boar_hid)
        
        if len(res) == 0:
            result =  {
                'result':{
                    'num':  ERROR_SOW_BOAR_MATE_INVALID_PARENT_BOAR_HASHID,
                    'code': 'ERROR_SOW_BOAR_MATE_INVALID_PARENT_BOAR_HASHID'
                }
            }
        
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
        
            return result
        
        parent_boar_id = res[0]
        
    
    
    sow_boar_mate_data.user_id       = user_id
    sow_boar_mate_data.pig_farm_id   = pig_farm_id
    sow_boar_mate_data.parent_sow_id = parent_sow_id
    sow_boar_mate_data.parent_boar_id= parent_boar_id
    sow_boar_mate_data.number        = number
    sow_boar_mate_data.name          = name
    
    
    res_add    =  model['sow_boar_mate'].add(sow_boar_mate_data)
    
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
    

@app.post("/sow_boar_mate/update", tags=["Sow Boar"])
async def sow_boar_mate_update(sow_boar_mate_data: dm.DataSowBoarMate):
    uhid        = sow_boar_mate_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    res_check = check_if_valid_user_account(user_id)
    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    sow_boar_mate_hid    = sow_boar_mate_data.sow_boar_mate_hid
    res = hashids_common.decrypt(sow_boar_mate_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_MATE_INVALID_HASHID,
                'code': 'ERROR_SOW_BOAR_MATE_INVALID_HASHID'
            }
        }
    
    sow_boar_mate_id = res[0]
    
    
    
    parent_sow_id       = 0
    parent_sow_hid      = sow_boar_mate_data.parent_sow_hid
    
    if parent_sow_hid is not None:
        res = hashids_common.decrypt(parent_sow_hid)
        
        if len(res) == 0:
            result =  {
                'result':{
                    'num':  ERROR_SOW_BOAR_MATE_INVALID_PARENT_SOW_HASHID,
                    'code': 'ERROR_SOW_BOAR_MATE_INVALID_PARENT_SOW_HASHID'
                }
            }
        
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
        
            return result
        
        parent_sow_id = res[0]
        
    
    parent_boar_id      = 0
    parent_boar_hid     = sow_boar_mate_data.parent_boar_hid
    
    if parent_boar_hid is not None:
        res = hashids_common.decrypt(parent_boar_hid)
        
        if len(res) == 0:
            result =  {
                'result':{
                    'num':  ERROR_SOW_BOAR_MATE_INVALID_PARENT_BOAR_HASHID,
                    'code': 'ERROR_SOW_BOAR_MATE_INVALID_PARENT_BOAR_HASHID'
                }
            }
        
            if new_bill_hid is not None:
                result['result']['new_bill_hid'] = new_bill_hid
        
            return result
        
        parent_boar_id = res[0]
        
    
    
    
    sow_boar_mate_data.user_id       = user_id
    sow_boar_mate_data.sow_boar_mate_id   = sow_boar_mate_id
    sow_boar_mate_data.parent_sow_id = parent_sow_id
    sow_boar_mate_data.parent_boar_id= parent_boar_id
    
    
    
    res_update  =  model['sow_boar_mate'].update(sow_boar_mate_data)
    
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
    

def get_data_sow_boar_mate_list(sow_boar_id, is_external = 0):
    res = model['sow_boar_mate'].get_list(sow_boar_id, is_external)
    
    
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

    return res


@app.get("/sow_boar_mate/list", tags=["Sow Boar"])
async def sow_boar_mate_list(sow_boar_hid:str, is_external:int = 0):
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
    
    sow_boar_id = 0
    
    res = hashids_common.decrypt(sow_boar_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_MATE_INVALID_SOW_BOAR_HASHID,
                'code': 'ERROR_SOW_BOAR_MATE_INVALID_SOW_BOAR_HASHID'
            }
        }
    
    sow_boar_id = res[0]
    
    
    res = get_data_sow_boar_mate_list(sow_boar_id, is_external)
            
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
        
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }

