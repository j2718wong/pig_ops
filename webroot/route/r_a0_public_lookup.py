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

   
@app.get("/lookup/feed_type/list", tags=["Common Lookup"])
async def lookup_feed_type_list():
    """
    Will get feed_type list.
    
    Parameters
    ----------
    
   
    """
    
        
    res = model['public_lookup'].get_list_feed_type()
    
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
    
    
   
@app.get("/lookup/harvest_type/list", tags=["Common Lookup"])
async def lookup_harvest_type_list():
    """
    Will get harvest_type list.
    
    Parameters
    ----------
    
   
    """
    
        
    res = model['public_lookup'].get_list_harvest_type()
    
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
    
    
