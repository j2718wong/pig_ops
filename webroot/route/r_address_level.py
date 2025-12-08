# August 23, 2025
# Jack Wong

import os
import sys
import json
import pprint

from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *





@app.get("/address/level_1/list", tags=["Location Address"])
async def address_level_1_list(country_id:int):
    """
    Will get address_level_1 list.
    
    Parameters
    ----------
    country_id : int
        country_id
    """
    

    res     = model['address_level'].get_address_level_1_list(country_id)
    
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
        cur_id    = cur_entry['id']
        cur_hid   = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid'] = cur_hid
    
            
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    

@app.get("/address/level_2/list", tags=["Location Address"])
async def address_level_2_list(adrs_level_1_id:int):
    """
    Will get address_level_2 list.
    
    Parameters
    ----------
    adrs_level_1_id : int
        adrs_level_1_id
    """
    

    res     = model['address_level'].get_address_level_2_list(adrs_level_1_id, 
        return_tuple)
    
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
        cur_id    = cur_entry['id']
        cur_hid   = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid'] = cur_hid
        
            
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    

@app.get("/address/level_3/list", tags=["Location Address"])
async def address_level_3_list(adrs_level_2_id:int):
    """
    Will get address_level_3 list.
    
    Parameters
    ----------
    adrs_level_2_id : int
        adrs_level_2_id
    """
    

    res     = model['address_level'].get_address_level_3_list(adrs_level_2_id)
    
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
    
    
@app.get("/address/level/names", tags=["Location Address"])
async def address_level_names(adrs_level_1_id:int = 0, 
    adrs_level_2_id:int = 0, adrs_level_3_id:int = 0):
    """
    Will get address_level names.
    
    Parameters
    ----------
    adrs_level_1_id : int
        adrs_level_1_id
    """
    res  = model['address_level'].get_address_level_names(
        address_level_1_id = adrs_level_1_id,
        address_level_2_id = adrs_level_2_id,
        address_level_3_id = adrs_level_3_id
    )
    
    return {
        'result': {
            'num':  0,
            'code': "SUCCESS"
        },
        
        'data': res
    
    }

