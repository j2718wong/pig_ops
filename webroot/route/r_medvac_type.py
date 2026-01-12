# January 12, 2026
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

    
@app.post("/medvac_type/add", tags=["Common Lookup"])
async def medvac_type_add(medvac_type_data: dm.DataMedVacType):
    name    = medvac_type_data.name
    uhid    = medvac_type_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_MEDVAC_BRAND_INVALID_NAME,
                'code': 'ERROR_MEDVAC_BRAND_INVALID_NAME'
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_MEDVAC_BRAND_INVALID_USER_HASHID,
                'code': 'ERROR_MEDVAC_BRAND_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    medvac_type_data.name      = name
    medvac_type_data.user_id   = user_id
    
    res_add    =  model['medvac_type'].add(medvac_type_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    medvac_type_id    = res_add['medvac_type']['id']
    medvac_type_hid   = hashids_common.encrypt(medvac_type_id)
    
    # remove plain id
    del res_add['medvac_type']['id']
    res_add['medvac_type']['hid'] = medvac_type_hid

        
    return res_add
    

   
@app.get("/medvac_type/list", tags=["Common Lookup"])
async def medvac_type_list():
    """
    Will get medvac_type list.
    
    Parameters
    ----------
    
    country_id:int
        country_id

    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    """
    
        
    res = model['medvac_type'].get_list()
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
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
            'code': 'SUCCESS'
        },
        
        'data': res
    }
    
    

    