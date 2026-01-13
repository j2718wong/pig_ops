# January 12, 2025
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

   
@app.post("/pig_medvac/add", tags=["Pig Details"])
async def pig_medvac_add(pig_medvac_data: dm.DataPigMedvac):
    name    = pig_medvac_data.name
    uhid    = pig_medvac_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_NAME,
                'code': 'ERROR_PIG_MEDVAC_INVALID_NAME'
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    sow_boar_id         = 0
    pig_prod_id         = 0         
    pig_prod_pig_ops_id = 0
    health_issue_id     = 0
    
    staff_id            = 0
    medvac_brand_id     = 0
    medvac_type_id      = 0
    
    
    
    sow_boar_hid        = pig_medvac_data.sow_boar_hid
    
    if sow_boar_hid is not None:
        res = hashids_common.decrypt(sow_boar_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_SOW_BOAR_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_SOW_BOAR_HASHID'
                }
            }
        
        sow_boar_id = res[0]
    
    
    
    pig_prod_hid        = pig_medvac_data.pig_prod_hid
    
    if pig_prod_hid is not None:
        res = hashids_common.decrypt(pig_prod_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_PIG_PROD_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_PIG_PROD_HASHID'
                }
            }
        
        pig_prod_id = res[0]
    
    
    
    pig_prod_pig_ops_hid = pig_medvac_data.pig_prod_pig_ops_hid
    
    if pig_prod_pig_ops_hid is not None:
        res = hashids_common.decrypt(pig_prod_pig_ops_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_PIG_PROD_PIG_OPS_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_PIG_PROD_PIG_OPS_HASHID'
                }
            }
        
        pig_prod_id = res[0]
    
    
    
    health_issue_hid        = pig_medvac_data.health_issue_hid
    
    if health_issue_hid is not None:
        res = hashids_common.decrypt(health_issue_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_HEALTH_ISSUE_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_HEALTH_ISSUE_HASHID'
                }
            }
        
        health_issue_id = res[0]
    
    
    

    staff_hid = pig_medvac_data.staff_hid
    
    if staff_hid is not None:
        res = hashids_common.decrypt(staff_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_MEDVAC_INVALID_STAFF_HASHID,
                    'code': 'ERROR_PIG_MEDVAC_INVALID_STAFF_HASHID'
                }
            }
        
        staff_id = res[0]
    
    
    medvac_brand_hid = pig_medvac_data.medvac_brand_hid
    
    res = hashids_common.decrypt(staff_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_MEDVAC_BRAND_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_MEDVAC_BRAND_HASHID'
            }
        }
    
    medvac_brand_id = res[0]
    
    
    medvac_type_hid = pig_medvac_data.medvac_type_hid
    
    res = hashids_common.decrypt(staff_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_MEDVAC_TYPE_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_MEDVAC_TYPE_HASHID'
            }
        }
    
    medvac_type_id = res[0]
    
    
    
    pig_medvac_data.name            = name
    pig_medvac_data.sow_boar_id     = sow_boar_id
    pig_medvac_data.pig_prod_id     = pig_prod_id
    pig_medvac_data.pig_prod_pig_ops_id = pig_prod_pig_ops_id
    pig_medvac_data.health_issue_id = health_issue_id
    pig_medvac_data.staff_id        = staff_id
    pig_medvac_data.medvac_brand_id = medvac_brand_id
    pig_medvac_data.medvac_type_id  = medvac_type_id
    
    
    res_add    =  model['pig_medvac'].add(pig_medvac_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    cur_id    = res_add['pig_medvac']['id']
    cur_hid   = hashids_common.encrypt(cur_id)
    
    # remove plain id
    del res_add['pig_medvac']['id']
    res_add['pig_medvac']['hid'] = cur_hid

        
    return res_add
    

@app.post("/pig_medvac/update", tags=["Pig Details"])
async def pig_medvac_update(pig_medvac_data: dm.DataPigMedvac):
    name    = pig_medvac_data.name
    uhid    = pig_medvac_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_NAME,
                'code': 'ERROR_PIG_MEDVAC_INVALID_NAME'
            }
        }
        
       
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    pig_race_line_hid = pig_medvac_data.pig_race_line_hid
    
    res = hashids_common.decrypt(pig_race_line_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_HASHID,
                'code': 'ERROR_PIG_MEDVAC_HASHID'
            }
        }
    
    
    pig_race_line_id = res[0]
    
    
    pig_medvac_data.name      = name
    pig_medvac_data.user_id   = user_id
    pig_medvac_data.pig_race_line_id = pig_race_line_id
    
    res_update    =  model['pig_race_line'].update(pig_medvac_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
        
    # remove plain id
    del res_update['pig_race_line']['id']
    res_update['pig_race_line']['hid'] = pig_race_line_hid
        
    return res_update
    

@app.get("/pig_medvac/delete", tags=["Pig Details"])
async def pig_medvac_delete(uhid:str, ehid: str):
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(ehid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_INVALID_HASHID,
                'code': 'ERROR_PIG_MEDVAC_INVALID_HASHID'
            }
        }
    
    pig_race_line_id = res[0]
    
    
    
    data = {
        'user_id':              user_id,
        'pig_race_line_id':     pig_race_line_id
    }
    
    
    res_delete    =  model['pig_race_line'].delete(data)
    
    if res_delete is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_delete['pig_race_line']['id']
    res_delete['pig_race_line']['hid'] = ehid
        
    return res_delete
    
    
@app.get("/pig_medvac/list", tags=["Pig Details"])
async def pig_medvac_list(sow_boar_hid: str, inc_deleted: int = 0, inc_user_audit:int = 0):
    """
    Will get pig medvac list.
    
    Parameters
    ----------
    
    sow_boar_hid:str
        account hashid

    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    
    """
    
    
    res = hashids_common.decrypt(sow_boar_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_MEDVAC_SOW_BOAR_HASHID,
                'code': 'ERROR_PIG_MEDVAC_SOW_BOAR_HASHID'
            }
        }
    
    
    sow_boar_id = res[0]
        
    res = model['pig_medvac'].get_list(sow_boar_id, 
            inc_deleted, inc_user_audit)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['medvac']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['medvac']['id']
        cur_entry['medvac']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['medvac']['brand']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['medvac']['brand']['id']
        cur_entry['medvac']['brand']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['medvac']['type']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['medvac']['type']['id']
        cur_entry['medvac']['type']['hid']   = cur_hid
        
        
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    
    

    