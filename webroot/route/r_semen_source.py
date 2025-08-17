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


@app.get("/semen_source/list")
async def semen_source_list(pfhid):
    """
    Will get semen_source list.
    
    Parameters
    ----------

    """
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_INVALID_HASHID',
                'desc': ''
            }
        }
    
    
    pig_farm_id = res[0]
    
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    res = model['semen_source'].get_semen_source_list(pig_farm_id)
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }

    
@app.post("/semen_source/add")
async def semen_source_add(semen_source_data: dm.DataSemenSource):
    uhid        = semen_source_data.uhid
    
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
    
    
    pfhid       = semen_source_data.pfhid
    
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
    
    
    semen_source_data.user_id        = user_id
    semen_source_data.pig_farm_id    = pig_farm_id
    
    res_add    =  model['semen_source'].add(semen_source_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
    return res_add
    

@app.post("/semen_source/update")
async def semen_source_update(semen_source_data: dm.DataSemenSource):
    uhid        = semen_source_data.uhid
    
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
    
    
    pfhid       = semen_source_data.pfhid
    
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
    
    
    semen_source_data.user_id        = user_id
    semen_source_data.pig_farm_id    = pig_farm_id
    
    res_update  =  model['semen_source'].update(semen_source_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
    return res_update
    

@app.get("/semen_source/delete")
async def semen_source_delete(uhid:str, id:int):
    uhid        = semen_source_data.uhid
    
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
    
   
    res_delete      =  model['semen_source'].delete(user_id, id)
    
    if res_delete is None:
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
    
    res = model['semen_source'].get_sow_list(pig_farm_id)
    
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
    

@app.get("/semen_source/list")
async def semen_source_list(pfhid:str, sex:str = 'F', full_info: int = 0):
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
    
    
    res = model['semen_source'].get_semen_source_list(pig_farm_id, sex)
    
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

    