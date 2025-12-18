# August 24, 2025
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


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)


from r_utils                import get_location_address_names_and_replace_ids


    
@app.post("/semen_supplier/add", tags=["Common Lookup"])
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
    
    
    
    level_1_id  = 0
    level_2_id  = 0
    level_3_id  = 0
    
    
    level_1_hid = feed_supplier_data.level_1_hid
    res = hashids_common.decrypt(level_1_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SUPPLIER_INVALID_ADDRESS_LEVEL_1,
                'code': 'ERROR_SEMEN_SUPPLIER_INVALID_ADDRESS_LEVEL_1',
                'desc': ''
            }
        }
        
    level_1_id = res[0]
    
    
    level_2_hid = feed_supplier_data.level_2_hid
    res = hashids_common.decrypt(level_2_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SUPPLIER_INVALID_ADDRESS_LEVEL_2,
                'code': 'ERROR_SEMEN_SUPPLIER_INVALID_ADDRESS_LEVEL_2',
                'desc': ''
            }
        }
    
    level_2_id = res[0]
    
    
    level_3_hid = feed_supplier_data.level_3_hid
    
    if level_3_hid is not None:
        res = hashids_common.decrypt(level_3_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SEMEN_SUPPLIER_INVALID_ADDRESS_LEVEL_3,
                    'code': 'ERROR_SEMEN_SUPPLIER_INVALID_ADDRESS_LEVEL_3',
                    'desc': ''
                }
            }
        
        level_3_id = res[0]
    

    
    semen_supplier_data.name        = name
    semen_supplier_data.user_id     = user_id
    semen_supplier_data.level_1_id  = level_1_id
    semen_supplier_data.level_2_id  = level_2_id
    semen_supplier_data.level_3_id  = level_3_id
    
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
    res_add['semen_supplier']['hid'] = semen_supplier_hid

        
    return res_add
    

@app.post("/semen_supplier/update", tags=["Common Lookup"])
async def semen_supplier_update(semen_supplier_data: dm.DataSemenSupplier):
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
    
    
    semen_supplier_hid = semen_supplier_data.semen_supplier_hid
    
    res = hashids_common.decrypt(semen_supplier_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SEMEN_SUPPLIER_HASHID,
                'code': 'ERROR_SEMEN_SUPPLIER_HASHID',
                'desc': ''
            }
        }
    
    semen_supplier_id = res[0]
    
    
    semen_supplier_data.name      = name
    semen_supplier_data.user_id   = user_id
    semen_supplier_data.semen_supplier_id = semen_supplier_id
    
    res_update    =  model['semen_supplier'].update(semen_supplier_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    semen_supplier_id    = res_update['semen_supplier']['id']
    semen_supplier_hid   = hashids_common.encrypt(semen_supplier_id)
    
    # remove plain id
    del res_update['semen_supplier']['id']
    res_update['semen_supplier']['hid'] = semen_supplier_hid

        
    return res_update
    


@app.get("/semen_supplier/list", tags=["Common Lookup"])
async def semen_supplier_list(ahid:str = None, level_2_hid: str = None):
    """
    Will get semen_supplier list.
    
    Parameters
    ----------
    
    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    """
    
    account_id      = 0
    adrs_level_2_id = 0
    
    if level_2_hid is not None:
            
        res = hashids_common.decrypt(level_2_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_ADDRESS_LEVEL_2_HID,
                    'code': 'ERROR_ADDRESS_LEVEL_2_HID',
                    'desc': ''
                }
            }
        
        adrs_level_2_id = res[0]
        
        
        res = model['semen_supplier'].get_list(
                address_level_2_id  = adrs_level_2_id,
                minimum_info        = 1)

        
        if res is None:
            return {
                'result':{
                    'num':  ERROR_DATABASE_ERROR,
                    'code': 'ERROR_DATABASE_ERROR',
                    'desc': ''
                }
            }
    
    
        
    res = model['semen_supplier'].get_list(address_level_1_id, address_level_2_id)
    
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
        cur_id  = cur_entry['semen_supplier']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['semen_supplier']['id']
        cur_entry['semen_supplier']['hid']   = cur_hid
        
        
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    
    

    