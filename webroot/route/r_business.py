# April 12, 2026
# Jack Wong

import os
import sys
import pprint


from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse


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


from r_a0_security_checks   import check_if_valid_user_account
from r_utils                import remove_database_null_description

   
@app.get("/b/pricing/current", tags=["Business"])
async def b_pricing_current(request: Request, chid: str = None):
    """
    Will get current pricing.
    
    Parameters
    ----------
    
    chid:str
        country_hid of the account

    Returns
    -------
        list of default pricing and country_specific pricing
   
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    country_id = None
    
    if chid is not None:
    
        res = hashids_common.decrypt(chid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_ADDRESS_COUNTRY_HID,
                    'code': 'ERROR_ADDRESS_COUNTRY_HID'
                }
            }
        
        country_id = res[0]
        
    res = model['business'].get_pricing(country_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
            
    
    # Replace plain id
    for cur_entry in res:
        cur_id  = cur_entry['pricing']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pricing']['id']
        cur_entry['pricing']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['pricing']['country_id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pricing']['country_id']
        cur_entry['pricing']['country_hid']   = cur_hid
        
            
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }
    
    

    
