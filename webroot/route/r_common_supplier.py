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

    
@app.post("/supplier/add", tags=["Common Lookup"])
async def supplier_add(supplier_data: dm.DataCommonSupplier):
    name    = supplier_data.name
    uhid    = supplier_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_SUPPLIER_INVALID_NAME,
                'code': 'ERROR_SUPPLIER_INVALID_NAME'
            }
        }
    
    if  supplier_data.is_feed_supplier == 0 and \
        supplier_data.is_gilt_supplier == 0 and \
        supplier_data.is_semen_supplier == 0:
            
        return {
            'result':{
                'num':  ERROR_SUPPLIER_MUST_HAVE_AT_LEAST_SUPPLIER_FLAG,
                'code': 'ERROR_SUPPLIER_MUST_HAVE_AT_LEAST_SUPPLIER_FLAG'
            }
        }
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SUPPLIER_INVALID_USER_HASHID,
                'code': 'ERROR_SUPPLIER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    level_1_id  = 0
    level_2_id  = 0
    level_3_id  = 0
    
    
    level_1_hid = supplier_data.level_1_hid
    res = hashids_common.decrypt(level_1_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SUPPLIER_INVALID_ADDRESS_LEVEL_1,
                'code': 'ERROR_SUPPLIER_INVALID_ADDRESS_LEVEL_1'
            }
        }
        
    level_1_id = res[0]
    
    
    level_2_hid = supplier_data.level_2_hid
    res = hashids_common.decrypt(level_2_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SUPPLIER_INVALID_ADDRESS_LEVEL_2,
                'code': 'ERROR_SUPPLIER_INVALID_ADDRESS_LEVEL_2'
            }
        }
    
    level_2_id = res[0]
    
    
    level_3_hid = supplier_data.level_3_hid
    
    if level_3_hid is not None:
        res = hashids_common.decrypt(level_3_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SUPPLIER_INVALID_ADDRESS_LEVEL_3,
                    'code': 'ERROR_SUPPLIER_INVALID_ADDRESS_LEVEL_3'
                }
            }
        
        level_3_id = res[0]
    
    
    
    
    supplier_data.name         = name
    supplier_data.user_id      = user_id
    supplier_data.level_1_id   = level_1_id
    supplier_data.level_2_id   = level_2_id
    supplier_data.level_3_id   = level_3_id
    
    
    res_add    =  model['supplier'].add(supplier_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    #Replace Plain Id
    cur_id      = res_add['supplier']['id']
    cur_hid     = hashids_common.encrypt(cur_id)
    
    del res_add['supplier']['id']
    res_add['supplier']['hid']   = cur_hid
    
    
    get_location_address_names_and_replace_ids(res_add)
        
    
    return res_add
    

@app.post("/supplier/update", tags=["Common Lookup"])
async def supplier_update(supplier_data: dm.DataCommonSupplier):
    name    = supplier_data.name
    uhid    = supplier_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_SUPPLIER_INVALID_NAME,
                'code': 'ERROR_SUPPLIER_INVALID_NAME'
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SUPPLIER_INVALID_USER_HASHID,
                'code': 'ERROR_SUPPLIER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    supplier_hid = supplier_data.supplier_hid
    
    res = hashids_common.decrypt(supplier_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_SUPPLIER_HASHID,
                'code': 'ERROR_SUPPLIER_HASHID'
            }
        }
    
    supplier_id = res[0]
    
    
    level_3_id  = 0
    level_3_hid = supplier_data.level_3_hid
    
    if level_3_hid is not None:
        res = hashids_common.decrypt(level_3_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_SUPPLIER_INVALID_ADDRESS_LEVEL_3,
                    'code': 'ERROR_SUPPLIER_INVALID_ADDRESS_LEVEL_3'
                }
            }
        
        level_3_id = res[0]
    
    
    if  supplier_data.is_feed_supplier == 0 and \
        supplier_data.is_gilt_supplier == 0 and \
        supplier_data.is_semen_supplier == 0:
            
        return {
            'result':{
                'num':  ERROR_SUPPLIER_MUST_HAVE_AT_LEAST_SUPPLIER_FLAG,
                'code': 'ERROR_SUPPLIER_MUST_HAVE_AT_LEAST_SUPPLIER_FLAG'
            }
        }
    
    
    
    
    supplier_data.name          = name
    supplier_data.user_id       = user_id
    supplier_data.supplier_id   = supplier_id
    supplier_data.level_3_id    = level_3_id
    
    res_update      =  model['supplier'].update(supplier_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    del res_update['supplier']['id']
    res_update['supplier']['hid'] = supplier_hid
    
    get_location_address_names_and_replace_ids(res_update)
        
    return res_update
    

   
@app.get("/supplier/list", tags=["Common Lookup"])
async def supplier_list(ahid:str = None, level_2_hid: str = None,
    is_fs:int = 0, is_gs:int = 0, is_ss:int = 0):
    """
    Will get feed_supplier list.
    
    Parameters
    ----------
    ahid: str
        account_hid
    
    level_2_hid:str
        level_2_hid

    is_fs:int
        is_feed_supplier
        
    is_gs:int
        is_gilt_supplier
    
    is_ss:int
        is_semen_supplier
    
        

    """
    
    account_id      = 0
    adrs_level_2_id = 0
    
            
            
    if level_2_hid is not None:        
            
        res = hashids_common.decrypt(level_2_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_ADDRESS_LEVEL_2_HID,
                    'code': 'ERROR_ADDRESS_LEVEL_2_HID'
                }
            }
        
        level_2_id = res[0]
        
        
        res = model['supplier'].get_list(
                address_level_2_id  = level_2_id,
                is_feed_supplier    = is_fs, 
                is_gilt_supplier    = is_gs, 
                is_semen_supplier   = is_ss,
                minimum_info        = 1)

        
        if res is None:
            return {
                'result':{
                    'num':  ERROR_DATABASE_ERROR,
                    'code': 'ERROR_DATABASE_ERROR'
                }
            }
                
        
        # Replace plain id
        for cur_entry in res:
            cur_id      = cur_entry['id']
            cur_hid     = hashids_common.encrypt(cur_id)
            
            del cur_entry['id']
            cur_entry['hid']   = cur_hid
                
                
            cur_id      = cur_entry['level_3_id']
            if cur_id is not None: 
                cur_hid     = hashids_common.encrypt(cur_id)
            else:
                cur_hid     = None
            
            del cur_entry['level_3_id']
            cur_entry['level_3_hid']   = cur_hid
            
            
                
        return {
            'result':{
                'num':  0,
                'code': 'SUCCESS'
            },
            
            'data': res
        }
            
        
    
    if ahid is not None:
        res = hashids_account.decrypt(ahid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_SUPPLIER_INVALID_ACCOUNT_HASHID,
                    'code': 'ERROR_SUPPLIER_INVALID_ACCOUNT_HASHID'
                }
            }
        
        account_id = res[0]
        
        
        res = model['supplier'].get_list(
                account_id          = account_id, 
                is_feed_supplier    = is_fs, 
                is_gilt_supplier    = is_gs, 
                is_semen_supplier   = is_ss,
                minimum_info        = 0)

        
        if res is None:
            return {
                'result':{
                    'num':  ERROR_DATABASE_ERROR,
                    'code': 'ERROR_DATABASE_ERROR'
                }
            }
        

        # Replace plain id
        for cur_entry in res:
            get_location_address_names_and_replace_ids(cur_entry)
                
                
        return {
            'result':{
                'num':  0,
                'code': 'SUCCESS'
            },
            
            'data': res
        }
        
            
@app.get("/supplier/count", tags=["Common Lookup"])
async def supplier_count(country_id: int = 1, level_1_hid: str = None,
    is_fs:int = 0, is_gs:int = 0, is_ss:int = 0):
    """
    Will get supplier count.
    
    Parameters
    ----------
    
    level_1_hid: str
        address level 1 hashhid
    
    """
    
    level_1_id = None
    
    if level_1_hid is not None:
            
        res = hashids_common.decrypt(level_1_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_ADDRESS_LEVEL_1_HID,
                    'code': 'ERROR_ADDRESS_LEVEL_1_HID'
                }
            }
        
        level_1_id = res[0]
        
        
    res = model['supplier'].get_supplier_count(
        country_id          = country_id,
        address_level_1_id  = level_1_id)

    
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
    


    