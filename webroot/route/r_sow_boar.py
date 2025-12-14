# August 10, 2025
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel
from fastapi.responses      import HTMLResponse

from datetime               import datetime, timedelta

    
sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *


from fastapi.responses      import PlainTextResponse


import data_model           as dm


@app.get("/sow_boar", response_class = HTMLResponse, tags=["Sow Boar"])
async def sow_boar(pfhid:str = None):
    # Get the current logged in user;
    
    pig_farm_id = None
    
    if pfhid is not None:
        res = hashids_common.decrypt(pfhid)
        if len(res) == 0:
            # Just proceed if it is invalid; will get default 
            # account farm_id if not given
            test = 1
            
            """
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID',
                    'desc': ''
                }
            }
            """
        else:
            pig_farm_id = res[0]
            
    
    # temporary
    user_id = 1
   
    res_user = model['user'].get_user_info(user_id)
    if res_user == None:
        # TODO what to do in case no result
        return None
        
        
    # Get user.account_id 
    account_id = res_user['user']['account_id']
    
    # Get account info
    data_account = model['account'].get_info(account_id)
    if data_account == None:
        # TODO what to do in case no result
        return None
        
        
    # TODO Check account free trial period
        
    # TODO check account for not paid bill
    
        
    # Check if there is a farm_id list
    account_farm_ids = data_account['farm_ids']
    len_items = len(account_farm_ids)
    if len_items == 0:
        # TODO what to do in case no farm set
        return None
        
    if pig_farm_id is not None:
        # This is given by user 
        
        if pig_farm_id not in account_farm_ids:
            # TODO what to do in case farm_id given is not in account list
            return None
    
    else:
        # select the first farm_id
        pig_farm_id = account_farm_ids[0]
        
    
    
    # Get pig_farm sow list
    list_sow_list = model['sow_boar'].get_list(pig_farm_id, 'F', 
        is_disposed = 0, inc_external = 0, inc_user_audit = 1, 
        minimum_info = 0, order_by = 0)
    if list_sow_list == None:
        # TODO what to do in case no result
        return None
    
    
    # Get pig_farm boar list
    list_boar_list = model['sow_boar'].get_list(pig_farm_id, 'M', 
        is_disposed = 0, inc_external = 1, inc_user_audit = 1, 
        minimum_info = 0, order_by = 0)
    if list_boar_list == None:
        # TODO what to do in case no result
        return None
    

    for cur_entry in list_sow_list:
        cur_id      = cur_entry['sow_boar']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['sow_boar']['id']
        cur_entry['sow_boar']['hid']   = cur_hid
    
    
    for cur_entry in list_boar_list:
        cur_id      = cur_entry['sow_boar']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['sow_boar']['id']
        cur_entry['sow_boar']['hid']   = cur_hid

    
    page_data = {
        'account':                  data_account,
        
        'sow_list':                 list_sow_list,
        'boar_list':                list_boar_list
      
    }
    

    page = controller.view['sow_boar'].render(page_data = json.dumps(page_data, indent=4))
    
    return page
    

    
    
    
@app.get("/sow_status/list", tags=["Sow Boar"])
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
    
    
@app.post("/sow_boar/add", tags=["Sow Boar"])
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
       
            
            
    sow_boar_name       = sow_boar_data.name
    if sow_boar_name is not None:
        name        = sow_boar_name.strip()
        
    
    if name is None and number is None:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_NO_SOW_BOAR_NUMBER_OR_NAME,
                'code': 'ERROR_SOW_BOAR_NO_SOW_BOAR_NUMBER_OR_NAME',
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
    

@app.post("/sow_boar/update", tags=["Sow Boar"])
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
    

@app.post("/sow_boar/dispose", tags=["Sow Boar"])
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


@app.get("/sow/pt_list", response_class=PlainTextResponse, tags=["Sow Boar"])
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
                'num':  ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID',
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
    

@app.get("/sow_boar/list", tags=["Sow Boar"])
async def sow_boar_list(pfhid:str, sex:str = None, is_disposed: int = 0, 
        inc_external:int = 0, is_production_ready:int = 1, 
        inc_user_audit:int = 0, order_by:int = 0):
    """
    Will get sow list.
    
    Parameters
    ----------
    sex: str
        F = sow entries
        M = boar entries
    
    is_disposed:int
        0 = will return active sows, boars only; 
        1 = will return disposed sows, boars
        
    inc_external: int
        0 = will not include externally owned sow/boar
        1 = will include externally owned sow/boar
    
    is_production_ready: int
        0 = will  return gilts, junior boar
        1 = will return productin ready sowboar
        
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
                'num':  ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_PIG_FARM_HASHID',
                'desc': ''
            }
        }
    
    pig_farm_id = res[0]
    
    

    
    res = model['sow_boar'].get_list(pig_farm_id, sex, 
            is_disposed     = is_disposed,
            inc_external    = inc_external,
            is_production_ready = is_production_ready,
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


@app.get("/sow/production_output", tags=["Sow Boar"])
async def sow_production_output(sowhid:str):
    """
    Will get sow production list.
    
    Parameters
    ----------
    sowhid: str
        sow hash id
    
   

    """
    
    
    res = hashids_common.decrypt(sowhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SOW_BOAR_INVALID_SOW_HASHID,
                'code': 'ERROR_SOW_BOAR_INVALID_SOW_HASHID',
                'desc': ''
            }
        }
    
    sow_id = res[0]
    
    
    res = model['pig_prod'].get_production_output(sow_id)
    
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
        cur_id  = cur_entry['pig_production']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_production']['id']
        cur_entry['hid']   = cur_hid
        
        if sow_id > 0:
            del cur_entry['sow']
        
        
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    