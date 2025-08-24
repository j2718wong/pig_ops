# August 24, 2025
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

    
@app.post("/semen_supplier/add")
async def semen_supplier_add(semen_supplier_data: dm.DataSemenSupplier):
    name    = semen_supplier_data.name
    uhid    = semen_supplier_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SUPPLIER_INVALID_NAME,
                'code': 'ERROR_SEMEN_SUPPLIER_INVALID_NAME',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SUPPLIER_INVALID_USER_HASHID,
                'code': 'ERROR_SEMEN_SUPPLIER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    semen_supplier_data.name      = name
    semen_supplier_data.user_id   = user_id
    
    res_add    =  model['semen_supplier'].add(semen_supplier_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    semen_supplier_id    = res_add['semen_supplier']['id']
    semen_supplier_hid   = hashids_common.encrypt(semen_supplier_id)
    
    # remove plain id
    del res_add['semen_supplier']['id']
    res_add['semen_supplier']['h_id'] = semen_supplier_hid

        
    return res_add
    

   
@app.get("/semen_supplier/list")
async def semen_supplier_list(country_id: int = 1, adrs_level_1_id: int = None, 
        inc_deleted: int = 0, inc_user_audit:int = 0):
    """
    Will get semen_supplier list.
    
    Parameters
    ----------
    
    country_id:int
        country_id

    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    """
    
        
    res = model['semen_supplier'].get_list(country_id, adrs_level_1_id,
            inc_deleted, inc_user_audit)
    
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
    
    

    