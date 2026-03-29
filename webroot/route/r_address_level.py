# August 23, 2025
# Jack Wong

import os
import sys
import json
import pprint


from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse


from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *




@app.get("/address/level_1/list", tags=["Location Address"])
async def address_level_1_list(request: Request, country_hid:str):
    """
    Will get address_level_1 list.
    
    Parameters
    ----------
    country_id : int
        country_id
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    country_id = 0
    
            
    res = hashids_common.decrypt(country_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_ADDRESS_COUNTRY_HID,
                'code': 'ERROR_ADDRESS_COUNTRY_HID'
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
            'num':  0
        },
        
        'data': res
    }
    

@app.get("/address/level_2/list", tags=["Location Address"])
async def address_level_2_list(request: Request, level_1_hid:str):
    """
    Will get address_level_2 list.
    
    Parameters
    ----------
    level_1_hid : str
        adrs_level_1 hashid
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
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
                'code': 'ERROR_DATABASE_ERROR'
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
            'num':  0
        },
        
        'data': res
    }
    

@app.get("/address/level_3/list", tags=["Location Address"])
async def address_level_3_list(request: Request, level_2_hid:str):
    """
    Will get address_level_3 list.
    
    Parameters
    ----------
    level_2_hid : str
        adrs_level_2 hashid
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    adrs_level_2_id = 0
    
            
    res = hashids_common.decrypt(level_2_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_ADDRESS_LEVEL_2_HID,
                'code': 'ERROR_ADDRESS_LEVEL_2_HID'
            }
        }
    
    adrs_level_2_id = res[0]
    


    res     = model_la['address_level'].get_address_level_3_list(adrs_level_2_id)
    
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
            'num':  0
        },
        
        'data': res
    }
    
    
@app.get("/address/level/names", tags=["Location Address"])
async def address_level_names(request: Request, adrs_level_1_id:int = 0, 
    adrs_level_2_id:int = 0, adrs_level_3_id:int = 0):
    """
    Will get address_level names.
    
    Parameters
    ----------
    adrs_level_1_id : int
        adrs_level_1_id
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res  = model_la['address_level'].get_address_level_names(
        address_level_1_id = adrs_level_1_id,
        address_level_2_id = adrs_level_2_id,
        address_level_3_id = adrs_level_3_id
    )
    
    return {
        'result': {
            'num':  0
        },
        
        'data': res
    
    }

