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

  


@app.get("/pf_sow_due_chklst", tags=["Pig Farm"])
async def pig_farm_sow_due_chklst(request: Request, pfhid: str):
    """
    Will get pig farm sow due checklist list.
    
    Parameters
    ----------
    
    pfhid:str
        pig_farm  sow due checklist hid

        
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_INVALID_HASHID'
            }
        }
        
        return result
        
    pig_farm_id = res[0]


    res = model['pf_sow_due_chklst'].get_active_list(pig_farm_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # Replace plain id
    for cur_entry in res:
        # Replace plain ids
        cur_id     = cur_entry['id']
        cur_hid    = hashids_common.encrypt(cur_id)
        
    
        del cur_entry['id']
        cur_entry['hid'] = cur_hid


    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }



@app.post("/pf_sow_due_chklst_item/update", tags=["Pig Farm"])
async def pf_sow_due_chklst_item_update(request: Request, data: dm.DataPigFarmChecklistItem):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    checklist_item_hid = data.checklist_item_hid
    res = hashids_common.decrypt(checklist_item_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_MEDVAC_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_MEDVAC_INVALID_HASHID'
            }
        }
    
    checklist_item_id = res[0]
    
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    

    
    
    data.user_id            = user_id
    data.checklist_item_id  = checklist_item_id

    
    res_update    =  model['pf_sow_due_chklst'].update_checklist_item(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
        
    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)

        
    return res_update

