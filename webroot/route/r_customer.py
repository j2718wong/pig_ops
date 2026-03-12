# March 12, 2026
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



   
@app.post("/cust_feedback/add", tags=["Account"])
async def cust_feedback_add(request: Request, data: dm.DataCustomerFeedback):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    if data.date_notes is None:
        dt_now          = datetime.now()
        dt_now_s        = dt_now.strftime('%Y-%m-%d')
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_NOTES_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    
    data.user_id     = user_id
    
    
    res_add    =  model['cust_feedback'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    cur_id    = res_add['customer_feedback']['id']
    cur_hid   = hashids_common.encrypt(cur_id)
    
    # remove plain id
    del res_add['customer_feedback']['id']
    res_add['customer_feedback']['hid'] = cur_hid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)

    
    return res_add
    
