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
async def sow_status_list(is_dispose: int = 0):
    """
    Will get sow status list.
    
    Parameters
    ----------

    """
    
    res = model['sow_boar'].get_sow_status_list()
    
    
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
    
    
@app.post("/sow_boar/add")
async def sow_boar_add(sow_boar_data: dm.DataSowBoar):
    uhid        = sow_boar_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_USER_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pfhid       = sow_boar_data.pfhid
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID',
                'desc': ''
            }
        }
    
    pig_farm_id = res[0]
    
    
    number  = None
    name    = None
    
    sow_boar_number     = sow_boar_data.number
    if sow_boar_number is not None:
        number      = sow_boar_number.strip()
        if len(number) == 0:
            return {
                'result':{
                    'num':  ERROR_SOW_BOAR_INVALID_SOW_BOAR_NUMBER,
                    'code': 'ERROR_SOW_BOAR_INVALID_SOW_BOAR_NUMBER',
                    'desc': ''
                }
            }
            
            
    sow_boar_name       = sow_boar_data.name
    if sow_boar_name is not None:
        name        = sow_boar_name.strip()
        if len(name) == 0:
            return {
                'result':{
                    'num':  ERROR_SOW_BOAR_INVALID_SOW_BOAR_NAME,
                    'code': 'ERROR_SOW_BOAR_INVALID_SOW_BOAR_NAME',
                    'desc': ''
                }
            }
    
    
    if name is None and number is None:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_NO_SOW_BOAR_NUMBER_AND_NAME,
                'code': 'ERROR_SOW_BOAR_NO_SOW_BOAR_NUMBER_AND_NAME',
                'desc': ''
            }
        }
    
    
    sow_boar_data.user_id       = user_id
    sow_boar_data.pig_farm_id   = pig_farm_id
    sow_boar_data.number        = number
    sow_boar_data.name          = name
    
    
    res_add    =  model['sow_boar'].add(sow_boar_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    sow_boar_id     = res_add['sow_boar']['id']
    sow_boar_hid    = hashids_common.encrypt(sow_boar_id)
    
    del res_add['sow_boar']['id']
    res_add['sow_boar']['hid'] = sow_boar_hid

        
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
        
    
    # remove plain id
    sow_boar_id     = res_update['sow_boar']['id']
    sow_boar_hid    = hashids_common.encrypt(sow_boar_id)
    
    del res_update['sow_boar']['id']
    res_update['sow_boar']['hid'] = sow_boar_hid
        
    return res_update
    

@app.post("/sow_boar/dispose")
async def sow_boar_dispose(sow_boar_data: dm.DataSowBoarDispose):
    uhid        = sow_boar_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_USER_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    sow_boar_hid    = sow_boar_data.sow_boar_hid
    res = hashids_common.decrypt(sow_boar_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    sow_boar_id = res[0]
    
    
    sow_boar_data.user_id       = user_id
    sow_boar_data.sow_boar_id   = sow_boar_id
    
    res_dispose     =  model['sow_boar'].dispose(sow_boar_data)
    
    if res_dispose is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
    
    # remove plain id
    sow_boar_id     = res_dispose['sow_boar']['id']
    sow_boar_hid    = hashids_common.encrypt(sow_boar_id)
    
    del res_dispose['sow_boar']['id']
    res_dispose['sow_boar']['hid'] = sow_boar_hid
        
    return res_dispose


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
async def sow_boar_list(pfhid:str, sex:str = None, full_info: int = 0, 
        inc_user_audit:int = 0, order_by:int = 0):
    """
    Will get sow list.
    
    Parameters
    ----------
    sex: str
        F = sow entries
        M = boar entries
    
    full_info:int
        0 = will return active sows, boars only; 
        1 = will return including disposed sows, boars
        
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    order_by : int
            0 = ORDER BY date_of_birth DESC
            1 = ORDER BY id ASC

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
    
    
    inc_disposed = 0
    if full_info > 0:
        inc_disposed = 1
    
    res = model['sow_boar'].get_list(pig_farm_id, sex, 
            inc_disposed    = inc_disposed, 
            inc_user_audit  = inc_user_audit,
            order_by        = order_by)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
        
        
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }

    