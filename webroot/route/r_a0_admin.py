# May 12, 2026
# Jack Wong

import os
import sys
import pprint


from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse, PlainTextResponse, Response


from datetime               import datetime, timedelta, date

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *



@app.get("/admin/receipts", response_class = HTMLResponse,  tags=["Admin"])
async def admin_receipts(response: Response):
    
    page = controller.view['receipts'].render()
    
    return page


@app.get("/admin/payment_channel/list", tags=["Admin"])
async def payment_channel_list(request: Request ):
    """
    Will get pig_production status list.
    
    Parameters
    ----------

    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    res = model['admin'].get_payment_channels_list()
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
   
   # No need to convert plain_ids to hash_ids since this is an internal data     
   
    
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }




@app.get("/admin/receipts_load")
async def admin_receipts_load(request: Request):
    result = get_uhid_or_redirect(request)
    
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ADMIN_INVALID_USER_HASHID,
                'code': 'ERROR_ADMIN_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    # Check if user allowed to get this data
    user_account    = model['user'].get_user_account_info(user_id)


    # Check if the account is an company owned account
    account_flag    = user_account['account']['flag']
    
    if account_flag & FLAG_BIT_ACCOUNT_IS_COMPANY_OWNED == 0:
        return {
            'result':{
                'num':  ERROR_ADMIN_INVALID_ACCOUNT,
                'code': 'ERROR_ADMIN_INVALID_ACCOUNT'
            }
        }
        
        
    # Check user
    user_flag       = user_account['user']['flag']
    if user_flag & FLAG_BIT_USER_IS_ACTIVE == 0:
        return {
            'result':{
                'num':  ERROR_ADMIN_INVALID_USER,
                'code': 'ERROR_ADMIN_INVALID_USER',
                'desc': 'User Inactive'
            }
        }


    if user_flag & FLAG_BIT_USER_IS_DELETED > 0:
        return {
            'result':{
                'num':  ERROR_ADMIN_INVALID_USER,
                'code': 'ERROR_ADMIN_INVALID_USER',
                'desc': 'User is Deleted'
            }
        }

    
    if user_flag & FLAG_BIT_USER_IS_INTERNAL_DATA_ENTRY == 0:
        return {
            'result':{
                'num':  ERROR_ADMIN_INVALID_USER,
                'code': 'ERROR_ADMIN_INVALID_USER',
                'desc': 'Insufficient privilege'
            }
        }


    
    res = model['admin'].get_uploaded_receipts_for_reading()
    
    
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }
