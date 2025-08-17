# August 10, 2025
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


from fastapi.responses      import PlainTextResponse


import data_model           as dm


@app.get("/sow_status/list")
async def sow_status_list():
    """
    Will get sow status list.
    
    Parameters
    ----------

    """
    
    return model['sow'].get_sow_status_list()
    
    
@app.post("/sow/add")
async def sow_add(sow_data: dm.DataSow):
    uhid        = sow_data.uhid
    
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
    
    
    pfhid       = sow_data.pfhid
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_SOW_INVALID_PIG_FARM_HASHID',
                'desc': ''
            }
        }
    
    pig_farm_id = res[0]
    
    
    sow_number   = sow_data.sow_number.strip()
    if len(sow_number) == 0:        
        return {
            'result':{
                'num':  ERROR_SOW_INVALID_SOW_NUMBER,
                'code': 'ERROR_SOW_INVALID_SOW_NUMBER',
                'desc': ''
            }
        }
    
    sow_data.sow_number     = sow_number
    sow_data.user_id        = user_id
    sow_data.pig_farm_id    = pig_farm_id
    
    res_add    =  model['sow'].add(sow_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
    return res_add
    

@app.post("/sow/update")
async def sow_update(sow_data: dm.DataSow):
    uhid        = sow_data.uhid
    
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
    
        
    sow_number   = sow_data.sow_number.strip()
    if len(sow_number) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_INVALID_SOW_NUMBER,
                'code': 'ERROR_SOW_INVALID_SOW_NUMBER',
                'desc': ''
            }
        }
    
    sow_data.sow_number     = sow_number
    sow_data.user_id        = user_id
    
    res_update  =  model['sow'].update(sow_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
    return res_update
    

@app.post("/sow/cull")
async def sow_update(sow_data: dm.DataSowCull):
    uhid        = sow_data.uhid
    
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
    
    
    sow_data.user_id        = user_id
    
    res_cull    =  model['sow'].cull(sow_data)
    
    if res_cull is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
    return res_cull



@app.get("/sow/pt_list", response_class=PlainTextResponse)
async def sow_pt_list(pfhid, full_info: int = 0):
    """
    Will get sow list.
    
    Parameters
    ----------
    
    full_info:int
        0 = will return active sows only; 
        1 = will return including culled sows

        
    """
    
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_SOW_INVALID_PIG_FARM_HASHID',
                'desc': ''
            }
        }
    
    pig_farm_id = res[0]
    
    res = model['sow'].get_sow_list(pig_farm_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    s = DB_INFO + '\n\n'
        
    s += 'Sow_Num   Sow_Name     Date of Birth   SOW_Status   Date Culled   Notes\n'
    
   
    
    for cur_entry in res:
        
        if full_info == 0:
            if cur_entry['date_culled'] is not None:
                continue
        
        s_temp      = cur_entry['sow_number']
        num_chars   = len(s_temp)
        num_space   = 7 - num_chars
        s           += ' ' * num_space + s_temp
        s           += '   '
    
    
        s_temp      = cur_entry['sow_name']
        num_chars   = len(s_temp)
        num_space   = 10 - num_chars
        s           += s_temp + ' ' * num_space
        s           += '   '
    
    
        s_temp      = cur_entry['date_of_birth']
        s           += s_temp
        s           += '      '
        
        
        s_temp      = cur_entry['status']
        num_chars   = len(s_temp)
        num_space   = 10 - num_chars
        s           +=  s_temp + ' ' * num_space
        s           += '   '
    
        
        s_temp      = '          '   
        if cur_entry['date_culled'] is not None:
            s_temp  = cur_entry['date_culled']
        s           += s_temp
        s           += '    '
        
        s_temp      = '          '
        if cur_entry['notes'] is not None:
            s_temp  = cur_entry['notes']
        s           += s_temp
        s           += '    '
        
        
        s           += '\n'
        
    return s
    

@app.get("/sow/list")
async def sow_list(pfhid:str, full_info: int = 0):
    """
    Will get sow list.
    
    Parameters
    ----------
    
    full_info:int
        0 = will return active sows only; 
        1 = will return including culled sows

        
    """
    
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_SOW_INVALID_PIG_FARM_HASHID',
                'desc': ''
            }
        }
    
    pig_farm_id = res[0]
    
    
    res = model['sow'].get_sow_list(pig_farm_id)
    
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

    