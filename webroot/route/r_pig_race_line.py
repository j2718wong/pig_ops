# August 23, 2025
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import data_model           as dm


FLAG_BIT_USER_IS_ACTIVE                 = 1
FLAG_BIT_USER_EMAIL_VERIFIED            = 2
FLAG_BIT_USER_MOBILE_NUM_VERIFIED       = 4


ACCOUNT_REQUEST_ADD_USER_RES_NUM_SUCCESS            = 0
ACCOUNT_REQUEST_APPROVE_ADD_USER_RES_NUM_SUCCESS    = 0

    
@app.post("/pig_race_line/add")
async def pig_race_line(pig_race_line_data: dm.DataPigRaceLine):
    name    = pig_race_line_data.name
    uhid    = pig_race_line_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_RACE_LINE_INVALID_NAME,
                'code': 'ERROR_PIG_RACE_LINE_INVALID_NAME',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_GESTATING_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACC_GESTATING_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_race_line_data.name      = name
    pig_race_line_data.user_id   = user_id
    
    res_add    =  model['pig_race_line'].add(pig_race_line_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    pig_race_line_id    = res_add['pig_race_line']['id']
    pig_race_line_hid   = hashids_common.encrypt(pig_race_line_id)
    
    # remove plain id
    del res_add['pig_race_line']['id']
    res_add['pig_race_line']['h_id'] = pig_race_line_hid

        
    return res_add
    

@app.post("/pig_race_line/update")
async def pig_race_line_update(pig_race_line_data: dm.DataPigRaceLine):
    name    = pig_race_line_data.name
    uhid    = pig_race_line_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_RACE_LINE_INVALID_NAME,
                'code': 'ERROR_PIG_RACE_LINE_INVALID_NAME',
                'desc': ''
            }
        }
        
       
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_GESTATING_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_ACC_GESTATING_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_race_line_hid = pig_race_line_data.pig_race_line_hid
    
    
    res = hashids_common.decrypt(pig_race_line_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_RACE_LINE_HASHID,
                'code': 'ERROR_PIG_RACE_LINE_HASHID',
                'desc': ''
            }
        }
    
    
    pig_race_line_id = res[0]
    
    
    pig_race_line_data.name      = name
    pig_race_line_data.user_id   = user_id
    pig_race_line_data.pig_race_line_id = pig_race_line_id
    
    res_update    =  model['pig_race_line'].update(pig_race_line_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['pig_race_line']['id']
    res_update['pig_race_line']['h_id'] = pig_race_line_hid
        
    return res_update
    
    
@app.get("/pig_race_line/list")
async def pig_race_line_list(ahid: str):
    """
    Will get pig_race_line list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid

        
    """
    
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACC_GESTATING_OPS_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_ACC_GESTATING_OPS_INVALID_ACCOUNT_HASHID',
                'desc': ''
            }
        }
    
    
    account_id = res[0]
        
    res = model['pig_race_line'].get_pig_race_line_list(account_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
            
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    

    