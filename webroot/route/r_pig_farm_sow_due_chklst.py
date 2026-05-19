# May 19, 2026
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

from r_pig_farm_feed_buy    import replace_plain_ids_feed_item

  


@app.get("/pf_sow_due_chklst/list", tags=["Pig Farm"])
async def pig_farm_sow_due_chklst_list(request: Request, pf_chklst_hid: str):
    """
    Will get pig farm sow due checklist list.
    
    Parameters
    ----------
    
    pf_chklst_hid:str
        pig_farm  sow due checklist hid

        
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_common.decrypt(pf_feed_buy_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_FEED_BUY_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_PIG_FARM_HASHID'
            }
        }
        
        return result
        
    pf_feed_buy_id = res[0]


    res = model['pf_feed_buy'].get_list_items(pf_feed_buy_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    

    
    # Replace plain id
    for cur_entry in res:
        replace_plain_ids_feed_item(cur_entry)
        
        
            
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }

