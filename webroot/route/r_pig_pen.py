# August 23, 2025
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


import data_model           as dm

   
@app.post("/pig_pen/add")
async def pig_pen_add(request: Request, data: dm.DataPigPen):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    name    = data.name
    #uhid    = data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PIG_PEN_INVALID_NAME,
                'code': 'ERROR_PIG_PIG_PEN_INVALID_NAME',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PIG_PEN_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PIG_PEN_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    data.name      = name
    data.user_id   = user_id
    
    res_add    =  model['pig_pen'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    pig_pen_id    = res_add['pig_pen']['id']
    pig_pen_hid   = hashids_common.encrypt(pig_pen_id)
    
    # remove plain id
    del res_add['pig_pen']['id']
    res_add['pig_pen']['hid'] = pig_pen_hid

        
    return res_add
    

@app.post("/pig_pen/update")
async def pig_pen_update(request: Request, data: dm.DataPigPen):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    name    = data.name
    #uhid    = data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PIG_PEN_INVALID_NAME,
                'code': 'ERROR_PIG_PIG_PEN_INVALID_NAME',
                'desc': ''
            }
        }
        
       
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PIG_PEN_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PIG_PEN_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_pen_hid = data.pig_pen_hid
    
    
    res = hashids_common.decrypt(pig_pen_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PIG_PEN_HASHID,
                'code': 'ERROR_PIG_PIG_PEN_HASHID',
                'desc': ''
            }
        }
    
    
    pig_pen_id = res[0]
    
    
    data.name      = name
    data.user_id   = user_id
    data.pig_pen_id = pig_pen_id
    
    res_update    =  model['pig_pen'].update(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['pig_pen']['id']
    res_update['pig_pen']['hid'] = pig_pen_hid
        
    return res_update
    

@app.get("/pig_pen/delete")
async def pig_pen_delete(request: Request, ehid: str):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PIG_PEN_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PIG_PEN_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(ehid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PIG_PEN_INVALID_HASHID,
                'code': 'ERROR_PIG_PIG_PEN_INVALID_HASHID',
                'desc': ''
            }
        }
    
    pig_pen_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'pig_pen_id':     pig_pen_id
    }
    
    
    res_delete    =  model['pig_pen'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    # remove plain id
    del res_delete['pig_pen']['id']
    res_delete['pig_pen']['hid'] = ehid
        
    return res_delete
    
    
@app.get("/pig_pen/list")
async def pig_pen_list(request: Request, ahid: str, inc_deleted: int = 0, 
        inc_user_audit:int = 0):
    """
    Will get pig_pen list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid

    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PIG_PEN_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_PIG_PIG_PEN_INVALID_ACCOUNT_HASHID',
                'desc': ''
            }
        }
    
    
    account_id = res[0]
        
    res = model['pig_pen'].get_list(account_id, 
            inc_deleted, inc_user_audit)
    
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
        
        cur_pig_race_id  = cur_entry['pig_race']['id']
        cur_pig_race_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_race']['id']
        cur_entry['pig_race']['hid']   = cur_hid
        
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    

    
