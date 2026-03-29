# January 12, 2026
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


    
@app.post("/medvac_brand/add", tags=["Common Lookup"])
async def medvac_brand_add(request: Request, data: dm.DataMedVacBrand):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    name    = data.name
    #uhid    = data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_MEDVAC_BRAND_INVALID_NAME,
                'code': 'ERROR_MEDVAC_BRAND_INVALID_NAME'
            }
        }
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_MEDVAC_BRAND_INVALID_USER_HASHID,
                'code': 'ERROR_MEDVAC_BRAND_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    


    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']


    
    country_hid = data.country_hid
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

    
    data.country_id    = country_id
    data.name          = name
    data.user_id       = user_id
    
    res_add    =  model['medvac_brand'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    medvac_brand_id    = res_add['medvac_brand']['id']
    medvac_brand_hid   = hashids_common.encrypt(medvac_brand_id)
    
    # remove plain id
    del res_add['medvac_brand']['id']
    res_add['medvac_brand']['hid'] = medvac_brand_hid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)
        
        
    return res_add
    

   
@app.get("/medvac_brand/list", tags=["Common Lookup"])
async def medvac_brand_list(request: Request, country_hid: str):
    """
    Will get medvac_brand list.
    
    Parameters
    ----------
    
    country_id:int
        country_id

    inc_deleted: int
        if > 0, will include deleted entries
    
    inc_user_audit:
        if > 0, will include added_by and last_update info
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_common.decrypt(country_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_ADDRESS_COUNTRY_HID,
                'code': 'ERROR_ADDRESS_COUNTRY_HID'
            }
        }
    
    country_id = res[0]

        
    res = model['medvac_brand'].get_list(country_id)
    
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
    
    

    
