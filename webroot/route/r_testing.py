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

