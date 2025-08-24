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

    
@app.post("/feed_brand/add")
async def feed_brand_add(feed_brand_data: dm.DataFeedBrand):
    name    = feed_brand_data.name
    uhid    = feed_brand_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BRAND_INVALID_NAME,
                'code': 'ERROR_FEED_BRAND_INVALID_NAME',
                'desc': ''
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BRAND_INVALID_USER_HASHID,
                'code': 'ERROR_FEED_BRAND_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    feed_brand_data.name      = name
    feed_brand_data.user_id   = user_id
    
    res_add    =  model['feed_brand'].add(feed_brand_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    feed_brand_id    = res_add['feed_brand']['id']
    feed_brand_hid   = hashids_common.encrypt(feed_brand_id)
    
    # remove plain id
    del res_add['feed_brand']['id']
    res_add['feed_brand']['h_id'] = feed_brand_hid

        
    return res_add
    

   
@app.get("/feed_brand/list")
async def feed_brand_list(country_id: int = 1, inc_deleted: int = 0, 
        inc_user_audit:int = 0):
    """
    Will get feed_brand list.
    
    Parameters
    ----------
    
    country_id:int
        country_id

    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    """
    
        
    res = model['feed_brand'].get_list(country_id, 
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
    
    

    