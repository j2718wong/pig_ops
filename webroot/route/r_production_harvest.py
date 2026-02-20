# February 20, 2026
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


   
@app.post("/production_harvest/add", tags=["Production Details"])
async def prod_harvest_add(prod_harvest_data: dm.DataProductionHarvest):
    uhid    = prod_harvest_data.uhid
    
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PRODUCTION_HARVEST_INVALID_USER_HASHID,
                'code': 'ERROR_PRODUCTION_HARVEST_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    
    pig_prod_hid    = prod_harvest_data.pig_prod_hid

    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PRODUCTION_HARVEST_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_PRODUCTION_HARVEST_INVALID_PIG_PROD_HASHID'
            }
        }
    
    pig_prod_id = res[0]
    
    
    harvest_type_hid = prod_harvest_data.harvest_type_hid
    
    res = hashids_common.decrypt(harvest_type_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PRODUCTION_HARVEST_INVALID_TYPE_HASHID,
                'code': 'ERROR_PRODUCTION_HARVEST_INVALID_TYPE_HASHID'
            }
        }
    
    harvest_type_id = res[0]
    
    
    
    
    
    acc_pig_buyer_id    = 0
    acc_pig_buyer_hid   = prod_harvest_data.acc_pig_buyer_hid
    
    if acc_pig_buyer_hid is not None:
        res = hashids_common.decrypt(acc_pig_buyer_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PRODUCTION_HARVEST_INVALID_ACC_PIG_BUYER_HASHID,
                    'code': 'ERROR_PRODUCTION_HARVEST_INVALID_ACC_PIG_BUYER_HASHID'
                }
            }
        
        acc_pig_buyer_id = res[0]
    
   

   
    prod_harvest_data.user_id           = user_id
    prod_harvest_data.pig_prod_id       = pig_prod_id
    prod_harvest_data.harvest_type_id   = harvest_type_id
    prod_harvest_data.acc_pig_buyer_id  = acc_pig_buyer_id
    
    res_add    =  model['prod_harvest'].add(prod_harvest_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    prod_harvest_id    = res_add['prod_harvest']['id']
    prod_harvest_hid   = hashids_common.encrypt(prod_harvest_id)
    
    # remove plain id
    del res_add['prod_harvest']['id']
    res_add['prod_harvest']['hid'] = prod_harvest_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)

    
    return res_add
    

@app.post("/prod_harvest/update", tags=["Production Details"])
async def prod_harvest_update(prod_harvest_data: dm.DataProductionHarvest):
    uhid    = prod_harvest_data.uhid

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PRODUCTION_HARVEST_INVALID_USER_HASHID,
                'code': 'ERROR_PRODUCTION_HARVEST_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    prod_harvest_hid = prod_harvest_data.prod_harvest_hid
    
    res = hashids_common.decrypt(prod_harvest_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PRODUCTION_HARVEST_INVALID_HASHID,
                'code': 'ERROR_PRODUCTION_HARVEST_INVALID_HASHID'
            }
        }
    
    
    prod_harvest_id = res[0]
    
    
    harvest_type_hid = prod_harvest_data.harvest_type_hid
    
    res = hashids_common.decrypt(harvest_type_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PRODUCTION_HARVEST_INVALID_TYPE_HASHID,
                'code': 'ERROR_PRODUCTION_HARVEST_INVALID_TYPE_HASHID'
            }
        }
    
    harvest_type_id = res[0]
    
    
    
    acc_pig_buyer_id                    = 0
    prod_harvest_data.harvest_type_id   = harvest_type_id
    acc_pig_buyer_hid                   = prod_harvest_data.acc_pig_buyer_hid
    
    if acc_pig_buyer_hid is not None:
        res = hashids_common.decrypt(acc_pig_buyer_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PRODUCTION_HARVEST_INVALID_ACC_PIG_BUYER_HASHID,
                    'code': 'ERROR_PRODUCTION_HARVEST_INVALID_ACC_PIG_BUYER_HASHID'
                }
            }
        
        acc_pig_buyer_id = res[0]
    
   
    
    
    prod_harvest_data.user_id           = user_id
    prod_harvest_data.prod_harvest_id   = prod_harvest_id
    prod_harvest_data.harvest_type_id   = harvest_type_id
    prod_harvest_data.acc_pig_buyer_id  = acc_pig_buyer_id
    
    
    res_update    =  model['prod_harvest'].update(prod_harvest_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['prod_harvest']['id']
    res_update['prod_harvest']['hid'] = prod_harvest_hid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)

    
    return res_update
    

@app.get("/prod_harvest/delete", tags=["Production Details"])
async def prod_harvest_delete(uhid:str, ehid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PRODUCTION_HARVEST_INVALID_USER_HASHID,
                'code': 'ERROR_PRODUCTION_HARVEST_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(ehid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PRODUCTION_HARVEST_INVALID_HASHID,
                'code': 'ERROR_PRODUCTION_HARVEST_INVALID_HASHID'
            }
        }
    
    prod_harvest_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'prod_harvest_id':     prod_harvest_id
    }
    
    
    res_delete    =  model['prod_harvest'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['prod_harvest']['id']
    res_delete['prod_harvest']['hid'] = ehid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_delete)
    
    
    return res_delete
    
    
def get_data_prod_harvest(pig_prod_id):
            
    res = model['prod_harvest'].get_list(pig_prod_id)
    
    if res is None:
        return None
    
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['prod_harvest']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['prod_harvest']['id']
        cur_entry['prod_harvest']['hid']   = cur_hid
        
      
    return res
    
    
    
@app.get("/prod_harvest/list", tags=["Production Details"])
async def prod_harvest_list(pig_prod_hid: str = None):
    """
    Will get prod_harvest list.
    
    Parameters
    ----------
    
    pig_prod_hid:str
        pig_prod_hid hashid

   
    """
    
    pig_prod_id     = 0

    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PRODUCTION_HARVEST_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_PRODUCTION_HARVEST_INVALID_PIG_PROD_HASHID'
            }
        }
        
    pig_prod_id = res[0]
        
        
        
    res = get_data_prod_harvest(pig_prod_id)
    
    
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
    
    

    
