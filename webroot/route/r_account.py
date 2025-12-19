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


from r_utils                import get_location_address_names_and_replace_ids



ACCOUNT_REGISTER_RES_NUM_SUCCESS        = 0



@app.get("/account/info", tags=["Account"])
async def user_account_info(ahid: str):
    """
    Will get account info

    Parameters
    ----------
    ahid : str
        account hashid
    
    
    """
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_INVALID_HASHID',
                'desc': ''
            }
        }
    
    account_id = res[0]
    
    
    res = model['account'].get_info(account_id)
    
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    cur_id  = res['account']['id']
    cur_hid = hashids_account.encrypt(cur_id)
    
    del res['account']['id']
    res['account']['hid']   = cur_hid
    
        
    result = {
            'result':{
                'num':  0,
                'code': 'SUCCESS',
                'desc': ''
            }
        }
        
    result = result | res
    
    return result
        
        
        


@app.post("/account/register", tags=["Account"])
async def account_register(account_data: dm.DataAccount):
    name    = account_data.name
    uhid    = account_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    
    user_id = res[0]
    
    account_data.name       = name 
    account_data.user_id    = user_id
    
    res_register    =  model['account'].register(account_data)
    
    if res_register is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    account_id      = res_register['account']['id']
    account_flag    = res_register['account']['flag']
        
    account_hashid  = hashids_account.encrypt(account_id)
    
    # remove plain id
    del res_register['account']['id']
    res_register['account']['hid'] = account_hashid

    result_num      = res_register['result']['num']
    
    if result_num == ACCOUNT_REGISTER_RES_NUM_SUCCESS:
        data = {
           'account_id':    account_id,
           'hashid':        account_hashid
        }
        res_update = model['account'].update_hashid(data)
        
    return res_register
    
    
@app.post("/account/update", tags=["Account"])
async def account_update(account_data: dm.DataAccount):
    name    = account_data.name
    uhid    = account_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_INVALID_NAME,
                'code': 'ERROR_ACCOUNT_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    
    user_id = res[0]
    
    account_data.name       = name 
    account_data.user_id    = user_id
        
    res_update      =  model['account'].update(account_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    account_id      = res_update['account']['id']
    account_flag    = res_update['account']['flag']
        
    account_hashid  = hashids_account.encrypt(account_id)
    
    # remove plain id
    del res_update['account']['id']
    res_update['account']['hid'] = account_hashid

        
    return res_update
    
    
@app.post("/account/update_settings", tags=["Account"])
async def account_update_settings(account_settings_data: dm.DataAccountSettings):
    uhid    = account_settings_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    
    user_id = res[0]
    
    account_settings_data.user_id    = user_id
        
    res_update      =  model['account'].update_settings(account_settings_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    account_id      = res_update['account']['id']
        
    account_hashid  = hashids_account.encrypt(account_id)
    
    # remove plain id
    del res_update['account']['id']
    res_update['account']['hid'] = account_hashid

        
    return res_update

