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


@app.post("/semen_source/add")
async def semen_source_add(semen_source_data: dm.DataSemenSource):
    uhid        = semen_source_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SOURCE_INVALID_USER_HASHID,
                'code': 'ERROR_SEMEN_SOURCE_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pfhid           = semen_source_data.pfhid
    pig_farm_id     = 0
    
    if pfhid is not None:
        res = hashids_common.decrypt(pfhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SOURCE_INVALID_PIG_FARM_HASHID,
                    'code': 'ERROR_SEMEN_SOURCE_INVALID_PIG_FARM_HASHID',
                    'desc': ''
                }
            }
        
        pig_farm_id     = res[0]
        
    
    semen_source_data.user_id        = user_id
    semen_source_data.pig_farm_id    = pig_farm_id
    
    
    boar_hid        = semen_source_data.boar_hid
    boar_id         = None
    if boar_hid is not None:
        res = hashids_common.decrypt(boar_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SOURCE_INVALID_BOAR_HASHID,
                    'code': 'ERROR_SEMEN_SOURCE_INVALID_BOAR_HASHID',
                    'desc': ''
                }
            }
        
        boar_id     = res[0]
        
        
    semen_supplier_hid  = semen_source_data.semen_supplier_hid
    semen_supplier_id   = None
    if semen_supplier_hid is not None:
        res = hashids_common.decrypt(semen_supplier_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SOURCE_INVALID_SEMEN_SUPPLIER_HASHID,
                    'code': 'ERROR_SEMEN_SOURCE_INVALID_SEMEN_SUPPLIER_HASHID',
                    'desc': ''
                }
            }
        
        semen_supplier_id   = res[0]
        
    
    pig_race_line_hid   = semen_source_data.pig_race_line_hid
    pig_race_line_id    = None
    if pig_race_line_hid is not None:
        res = hashids_common.decrypt(pig_race_line_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SOURCE_INVALID_PIG_RACE_LINE_HASHID,
                    'code': 'ERROR_SEMEN_SOURCE_INVALID_PIG_RACE_LINE_HASHID',
                    'desc': ''
                }
            }
        
        pig_race_line_id   = res[0]
        
    
    if boar_id is not None:
        semen_source_data.boar_id   = boar_id
    
    else:
        if semen_supplier_id is None:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SOURCE_INVALID_SEMEN_SUPPLIER_HASHID,
                    'code': 'ERROR_SEMEN_SOURCE_INVALID_SEMEN_SUPPLIER_HASHID',
                    'desc': ''
                }
            }
            
        if pig_race_line_id is None:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SOURCE_INVALID_PIG_RACE_LINE_HASHID,
                    'code': 'ERROR_SEMEN_SOURCE_INVALID_PIG_RACE_LINE_HASHID',
                    'desc': ''
                }
            }
        
        semen_source_data.semen_supplier_id = semen_supplier_id
        semen_source_data.pig_race_line_id  = pig_race_line_id
        

    res_add    =  model['semen_source'].add(semen_source_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    semen_source_id    = res_add['semen_source']['id']
    semen_source_hid   = hashids_common.encrypt(semen_source_id)
        
    # remove plain id
    del res_add['semen_source']['id']
    res_add['semen_source']['hid'] = semen_source_hid
        
    return res_add
    

@app.post("/semen_source/update")
async def semen_source_update(semen_source_data: dm.DataSemenSource):
    uhid        = semen_source_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SOURCE_INVALID_USER_HASHID,
                'code': 'ERROR_SEMEN_SOURCE_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    semen_source_hid    = semen_source_data.semen_source_hid
    res = hashids_common.decrypt(semen_source_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SOURCE_INVALID_HASHID,
                'code': 'ERROR_SEMEN_SOURCE_INVALID_HASHID',
                'desc': ''
            }
        }
    
    semen_source_id = res[0]
    
        
    pfhid           = semen_source_data.pfhid
    pig_farm_id     = 0
    
    if pfhid is not None:
        res = hashids_common.decrypt(pfhid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SOURCE_INVALID_PIG_FARM_HASHID,
                    'code': 'ERROR_SEMEN_SOURCE_INVALID_PIG_FARM_HASHID',
                    'desc': ''
                }
            }
        
        pig_farm_id     = res[0]
        
    
    semen_source_data.user_id        = user_id
    semen_source_data.pig_farm_id    = pig_farm_id
    semen_source_data.semen_source_id = semen_source_id
    
    
    boar_hid        = semen_source_data.boar_hid
    boar_id         = None
    if boar_hid is not None:
        res = hashids_common.decrypt(boar_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SOURCE_INVALID_BOAR_HASHID,
                    'code': 'ERROR_SEMEN_SOURCE_INVALID_BOAR_HASHID',
                    'desc': ''
                }
            }
        
        boar_id     = res[0]
        
        
    semen_supplier_hid  = semen_source_data.semen_supplier_hid
    semen_supplier_id   = None
    if semen_supplier_hid is not None:
        res = hashids_common.decrypt(semen_supplier_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SOURCE_INVALID_SEMEN_SUPPLIER_HASHID,
                    'code': 'ERROR_SEMEN_SOURCE_INVALID_SEMEN_SUPPLIER_HASHID',
                    'desc': 'Cannot be decrypted'
                }
            }
        
        semen_supplier_id   = res[0]
        
    
    pig_race_line_hid   = semen_source_data.pig_race_line_hid
    pig_race_line_id    = None
    if pig_race_line_hid is not None:
        res = hashids_common.decrypt(pig_race_line_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SOURCE_INVALID_PIG_RACE_LINE_HASHID,
                    'code': 'ERROR_SEMEN_SOURCE_INVALID_PIG_RACE_LINE_HASHID',
                    'desc': ''
                }
            }
        
        pig_race_line_id   = res[0]
        
    
    if boar_id is not None:
        semen_source_data.boar_id   = boar_id
    
    else:
        if semen_supplier_id is None:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SOURCE_INVALID_SEMEN_SUPPLIER_HASHID,
                    'code': 'ERROR_SEMEN_SOURCE_INVALID_SEMEN_SUPPLIER_HASHID',
                    'desc': 'Semen Supplier cannot be empty'
                }
            }
            
        if pig_race_line_id is None:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SOURCE_INVALID_PIG_RACE_LINE_HASHID,
                    'code': 'ERROR_SEMEN_SOURCE_INVALID_PIG_RACE_LINE_HASHID',
                    'desc': ''
                }
            }
        
        semen_source_data.semen_supplier_id = semen_supplier_id
        semen_source_data.pig_race_line_id  = pig_race_line_id
    
    
    res_update  =  model['semen_source'].update(semen_source_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
    
    # remove plain id
    del res_update['semen_source']['id']
    res_update['semen_source']['hid'] = semen_source_hid
        
    return res_update
    

@app.get("/semen_source/delete")
async def semen_source_delete(uhid:str, semen_source_hid: str):
   
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
    
    
    res = hashids_common.decrypt(semen_source_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SOURCE_INVALID_HASHID,
                'code': 'ERROR_SEMEN_SOURCE_INVALID_HASHID',
                'desc': ''
            }
        }
    
    semen_source_id = res[0]
    
    data = {
        'user_id':          user_id,
        'semen_source_id':  semen_source_id
    }
    
    res_delete      =  model['semen_source'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
    
    # remove plain id
    del res_delete['semen_source']['id']
    res_delete['semen_source']['hid'] = semen_source_hid
        
    return res_delete


@app.get("/semen_source/list")
async def semen_source_list(ahid:str, inc_deleted: int = 0, 
        inc_user_audit:int = 0):
    """
    Will get semen_source list.
    
    Parameters
    ----------
    
    ahid:str
        account hashid
        
    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
        
    """
    
    res = hashids_account.decrypt(ahid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SOURCE_INVALID_ACCOUNT_HASHID,
                'code': 'ERROR_SEMEN_SOURCE_INVALID_ACCOUNT_HASHID',
                'desc': ''
            }
        }
    
    
    account_id = res[0]
    
    res = model['semen_source'].get_list(account_id,
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
        
        
        cur_pig_farm_id  = cur_entry['pig_farm']['id']
        cur_pig_farm_hid = hashids_common.encrypt(cur_pig_farm_id)
        
        del cur_entry['pig_farm']['id']
        cur_entry['pig_farm']['hid']   = cur_pig_farm_hid
        
        
        if 'boar' in cur_entry:
            cur_boar_id     = cur_entry['boar']['id']
            cur_boar_hid    = hashids_common.encrypt(cur_boar_id)
        
            del cur_entry['boar']['id']
            cur_entry['boar']['hid']   = cur_boar_hid
            
            
        if 'external_semen' in cur_entry:
            cur_supplier_id     = cur_entry['external_semen']['supplier_id']
            cur_supplier_hid    = hashids_common.encrypt(cur_supplier_id)
        
            del cur_entry['external_semen']['supplier_id']
            cur_entry['external_semen']['supplier_hid']   = cur_supplier_hid
    
            
            cur_pig_race_line_id  = cur_entry['external_semen']['pig_race_line']['id']
            cur_pig_race_line_hid = hashids_common.encrypt(cur_pig_race_line_id)
        
            del cur_entry['external_semen']['pig_race_line']['id']
            cur_entry['external_semen']['pig_race_line']['hid'] = cur_pig_race_line_hid
    
            
            
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }

    
