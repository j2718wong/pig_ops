# January 4, 2024
# Jack Wong

import os
import sys


from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse
    

from common_constants       import *
from common_app             import *
from common_fast_api        import *

    
@app.get("/testing/user/hashid/{user_id}", tags=["HashIds"])
async def testing_user_hashid(request: Request, user_id: int):
    """
    Will return hashid for user.id
    """
    
    return hashids_user.encrypt(user_id)
    

@app.get("/testing/account/hashid/{account_id}", tags=["HashIds"])
async def testing_account_hashid(request: Request, account_id: int):
    """
    Will return hashid for booking.id
    """
    
    return hashids_account.encrypt(account_id)
    
    
@app.get("/testing/common/hashid/{entry_id}", tags=["HashIds"])
async def testing_common_hashid(request: Request, entry_id: int):
    """
    Will return hashid for an id
    """
    
    return hashids_common.encrypt(entry_id)



@app.get("/testing/user/id/{user_hid}", tags=["HashIds"])
async def testing_user_id(request: Request, user_hid: str):
    """
    Will return user.id
    """
    
    res = hashids_user.decrypt(user_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    return {
        'user_hashid':  user_hid,
        'id':           user_id
    }
    

@app.get("/testing/account/id/{account_hid}", tags=["HashIds"])
async def testing_account_id(request: Request, account_hid: str):
    """
    Will return hashid for booking.id
    """
    
    res = hashids_account.decrypt(account_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_INVALID_HASHID'
            }
        }
    
    
    account_id = res[0]
    
    return {
        'account_hashid':  account_hid,
        'id':           account_id
    }
    
    
@app.get("/testing/common/id/{entry_hid}", tags=["HashIds"])
async def testing_common_id(request: Request, entry_hid: str):
    """
    Will return hashid for an id
    """
    
    res = hashids_common.decrypt(entry_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_INVALID_COMMON_HASHID,
                'code': 'ERROR_INVALID_COMMON_HASHID'
            }
        }
    
    
    entry_id = res[0]
    
    return {
        'entry_hashid':     entry_hid,
        'id':               entry_id
    }
    


