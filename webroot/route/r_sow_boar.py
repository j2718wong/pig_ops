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
    
    return model['sow_boar'].get_sow_status_list()
    
    
@app.post("/sow_boar/add")
async def sow_boar_add(sow_boar_data: dm.DataSowBoar):
    uhid        = sow_boar_data.uhid
    
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
    
    
    pfhid       = sow_boar_data.pfhid
    
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
    
    
    number   = sow_boar_data.number.strip()
    if len(number) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_INVALID_SOW_NUMBER,
                'code': 'ERROR_SOW_INVALID_SOW_NUMBER',
                'desc': ''
            }
        }
    
    sow_boar_data.number         = number
    sow_boar_data.user_id        = user_id
    sow_boar_data.pig_farm_id    = pig_farm_id
    
    res_add    =  model['sow_boar'].add(sow_boar_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
    return res_add
    

@app.post("/sow_boar/update")
async def sow_boar_update(sow_boar_data: dm.DataSowBoar):
    uhid        = sow_boar_data.uhid
    
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
    
        
    sow_boar_number   = sow_boar_data.number.strip()
    if len(sow_boar_number) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_SOW_NUMBER,
                'code': 'ERROR_SOW_BOAR_INVALID_SOW_NUMBER',
                'desc': ''
            }
        }
    
    sow_boar_data.number        = sow_boar_number
    sow_boar_data.user_id       = user_id
    
    res_update  =  model['sow_boar'].update(sow_boar_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
    return res_update
    

@app.post("/sow_boar/cull")
async def sow_boar_cull(sow_boar_data: dm.DataSowBoarCull):
    uhid        = sow_boar_data.uhid
    
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
    
    
    sow_boar_data.user_id        = user_id
    
    res_cull    =  model['sow_boar'].cull(sow_boar_data)
    
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
    
    res = model['sow_boar'].get_sow_list(pig_farm_id)
    
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
    

@app.get("/sow_boar/list")
async def sow_boar_list(pfhid:str, sex:str = 'F', full_info: int = 0):
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
    
    
    res = model['sow_boar'].get_sow_boar_list(pig_farm_id, sex)
    
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

    