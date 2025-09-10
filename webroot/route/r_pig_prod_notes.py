# August 29, 2025
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

   
@app.post("/pig_prod_notes/add")
async def pig_prod_notes_add(pig_prod_notes_data: dm.DataPigProdNotes):
    uhid    = pig_prod_notes_data.uhid
    
    if pig_prod_notes_data.date_notes is None:
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d')
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_prod_hid    = pig_prod_notes_data.pig_prod_hid
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_PIG_PROD_HASHID',
                'desc': ''
            }
        }
    
    pig_prod_id = res[0]
    
    
    pig_prod_notes_data.user_id     = user_id
    pig_prod_notes_data.pig_prod_id = pig_prod_id
    
    res_add    =  model['prod_notes'].add(pig_prod_notes_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    pig_prod_notes_id    = res_add['pig_prod_notes']['id']
    pig_prod_notes_hid   = hashids_common.encrypt(pig_prod_notes_id)
    
    # remove plain id
    del res_add['pig_prod_notes']['id']
    res_add['pig_prod_notes']['hid'] = pig_prod_notes_hid

        
    return res_add
    

@app.post("/pig_prod_notes/update")
async def pig_prod_notes_update(pig_prod_notes_data: dm.DataPigProdNotes):
    uhid    = pig_prod_notes_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_prod_notes_hid = pig_prod_notes_data.pig_prod_notes_hid
    
    res = hashids_common.decrypt(pig_prod_notes_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_HASHID',
                'desc': ''
            }
        }
    
    
    pig_prod_notes_id = res[0]
    
    
    pig_prod_notes_data.user_id   = user_id
    pig_prod_notes_data.pig_prod_notes_id = pig_prod_notes_id
    
    res_update    =  model['prod_notes'].update(pig_prod_notes_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    # remove plain id
    del res_update['pig_prod_notes']['id']
    res_update['pig_prod_notes']['hid'] = pig_prod_notes_hid
        
    return res_update
    

@app.get("/pig_prod_notes/delete")
async def pig_prod_notes_delete(uhid:str, pig_prod_notes_hid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(pig_prod_notes_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_HASHID',
                'desc': ''
            }
        }
    
    pig_prod_notes_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'pig_prod_notes_id':     pig_prod_notes_id
    }
    
    
    res_delete    =  model['pig_prod_notes'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    # remove plain id
    del res_delete['pig_prod_notes']['id']
    res_delete['pig_prod_notes']['hid'] = pig_prod_notes_hid
        
    return res_delete
    
    
@app.get("/pig_prod_notes/list")
async def pig_prod_notes_list(pig_prod_hid: str, inc_deleted: int = 0, inc_user_audit:int = 0):
    """
    Will get pig_prod_notes list.
    
    Parameters
    ----------
    
    pig_prod_hid:str
        pig_prod_hid hashid

    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_INVALID_PIG_PROD_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_PIG_PROD_HASHID',
                'desc': ''
            }
        }
    
    
    pig_prod_id = res[0]
        
    res = model['prod_notes'].get_list(pig_prod_id, inc_deleted, inc_user_audit)
    
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
        cur_id  = cur_entry['prod_notes']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['prod_notes']['id']
        cur_entry['prod_notes']['hid']   = cur_hid
        
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    

    