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

    
@app.post("/feed_supplier/add")
async def feed_supplier_add(feed_supplier_data: dm.DataFeedSupplier):
    name    = feed_supplier_data.name
    uhid    = feed_supplier_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_SUPPLIER_INVALID_NAME,
                'code': 'ERROR_FEED_SUPPLIER_INVALID_NAME',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_SUPPLIER_INVALID_USER_HASHID,
                'code': 'ERROR_FEED_SUPPLIER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    feed_supplier_data.name      = name
    feed_supplier_data.user_id   = user_id
    
    res_add    =  model['feed_supplier'].add(feed_supplier_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    feed_supplier_id    = res_add['feed_supplier']['id']
    feed_supplier_hid   = hashids_common.encrypt(feed_supplier_id)
    
    # remove plain id
    del res_add['feed_supplier']['id']
    res_add['feed_supplier']['hid'] = feed_supplier_hid

        
    return res_add
    

@app.post("/feed_supplier/update")
async def feed_supplier_update(feed_supplier_data: dm.DataFeedSupplier):
    name    = feed_supplier_data.name
    uhid    = feed_supplier_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_SUPPLIER_INVALID_NAME,
                'code': 'ERROR_FEED_SUPPLIER_INVALID_NAME',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_SUPPLIER_INVALID_USER_HASHID,
                'code': 'ERROR_FEED_SUPPLIER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    feed_supplier_hid = pig_race_line_data.feed_supplier_hid
    
    res = hashids_common.decrypt(feed_suplier_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_SUPPLIER_HASHID,
                'code': 'ERROR_FEED_SUPPLIER_HASHID',
                'desc': ''
            }
        }
    
    semen_supplier_id = res[0]
    
    
    feed_supplier_data.name      = name
    feed_supplier_data.user_id   = user_id
    feed_supplier_data.feed_supplier_hid = feed_supplier_hid
    
    res_update      =  model['feed_supplier'].update(feed_supplier_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    feed_supplier_id    = res_update['feed_supplier']['id']
    feed_supplier_hid   = hashids_common.encrypt(feed_supplier_id)
    
    # remove plain id
    del res_update['feed_supplier']['id']
    res_update['feed_supplier']['hid'] = feed_supplier_hid

        
    return res_update
    

   
@app.get("/feed_supplier/list")
async def feed_supplier_list(address_level_2_id: int):
    """
    Will get feed_supplier list.
    
    Parameters
    ----------
    
    address_level_2_id:int
        address_level_2_id

    """
    
        
    res = model['feed_supplier'].get_list(address_level_2_id)
    
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
    
    

    