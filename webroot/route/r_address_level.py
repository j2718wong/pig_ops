# August 23, 2025
# Jack Wong

import os
import sys
import json
import pprint



from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *





@app.get("/address/level_1/list", tags=["Location Address"])
async def address_level_1_list(country_hid:str):
    """
    Will get address_level_1 list.
    
    Parameters
    ----------
    country_id : int
        country_id
    """
    
    country_id = 0
    
            
    res = hashids_common.decrypt(country_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_ADDRESS_COUNTRY_HID,
                'code': 'ERROR_ADDRESS_COUNTRY_HID',
                'desc': ''
            }
        }
    
    country_id = res[0]

    

    res     = model_la['address_level'].get_address_level_1_list(country_id)
    
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
async def address_level_2_list(level_1_hid:str):
    """
    Will get address_level_2 list.
    
    Parameters
    ----------
    level_1_hid : str
        adrs_level_1 hashid
    """
    
    adrs_level_1_id = 0
    
            
    res = hashids_common.decrypt(level_1_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_ADDRESS_LEVEL_1_HID,
                'code': 'ERROR_ADDRESS_LEVEL_1_HID',
                'desc': ''
            }
        }
    
    adrs_level_1_id = res[0]
    

    res     = model_la['address_level'].get_address_level_2_list(adrs_level_1_id)
    
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
async def address_level_3_list(level_2_hid:str):
    """
    Will get address_level_3 list.
    
    Parameters
    ----------
    level_2_hid : str
        adrs_level_2 hashid
    """
    
    adrs_level_2_id = 0
    
            
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
    


    res     = model_la['address_level'].get_address_level_3_list(adrs_level_2_id)
    
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
    res  = model_la['address_level'].get_address_level_names(
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

