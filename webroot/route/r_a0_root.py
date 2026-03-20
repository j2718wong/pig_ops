# January 5, 2026
# Jack Wong

import os
import sys
import time
import pprint


import jwt

from fastapi                import Request, HTTPException, status, Depends, Response
from fastapi.responses      import HTMLResponse, RedirectResponse
from pydantic               import BaseModel


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


from r_utils                import (replace_plain_ids_user_account,
                                    get_browser_info)


from r_a0_security_checks   import get_user_account_info

from r_pig_production       import get_page_data_farm_account_pig_prod


PIG_FARM_ADD_RES_NUM_SUCCESS        = 0

COMBINED_LACTATING_PIG_OPS  = (PIG_OPERATION_TYPE_LACTATING_PIGLETS, 
                                PIG_OPERATION_TYPE_LACTATING_SOW)




@app.get("/signup", response_class = HTMLResponse, dependencies=[Depends(public_limit)])
async def signup(response: Response):
    # Add cache control headers to prevent caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    page = controller.view['signup'].render()
    
    return page
    


@app.get("/login", response_class = HTMLResponse, dependencies=[Depends(public_limit)])
async def signup(response: Response):
    # Add cache control headers to prevent caching
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    
    page = controller.view['signup'].render()
    
    return page
    


@app.get("/pig_farm/data")
async def pig_farm_data(request: Request):
    """
    2026-03-05 Notes:
    
    """
    
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        # redirect to PAGE_NOT_FOUND
        raise HTTPException(status_code=401, detail="Invalid token")
        
    user_id = res[0]
    
    
    pig_farm_data = get_farm_data(user_id)
    return pig_farm_data
    
    
def get_farm_data(user_id):
    time_init = time.time()
    
    data_app = get_application_data()
    
    user_account = get_user_account_info(user_id)
    
    
    if user_account is None:
        data = {
            'application':      data_app,
            'user_account':     None,
            'pig_farm_account': None
        }
        
        return {
            'result':{
                'num':  0,
                'code': 'SUCCESS'
            },
            
            'data': data
        }
       
    
    
    account = user_account['account']
    user    = user_account['user']
    
    if account is None:
        data = {
            'application':      data_app,
            'user_account':     user_account,
            'pig_farm_account': None
        }
        
        return {
            'result':{
                'num':  0,
                'code': 'SUCCESS'
            },
            
            'data': data
        }
    
    
    
    pig_farm_id = 0
    
    # Get user assigned farm id
    # This is the first pig_farm id in user.pig_farms
    #
    # It is possible that the user has user_id, account_id but no farm_ids.
    # This is because the user did not finish adding a pig farm
    # in the Add Pig Farm page. Users can do this.
    user_pig_farms = None
    
    if 'pig_farms' in user:
        user_pig_farms =  user['pig_farms']
    
    if user_pig_farms is not None and len(user_pig_farms) > 0:
        pig_farm_id = user_pig_farms[0]
    
    
    farm_account = None

    if pig_farm_id > 0:    
        farm_account = get_page_data_farm_account_pig_prod(
            pig_farm_id, inc_pig_prod = 0, inc_user_audit = 1)
        
    
    data = {
        'application':      data_app,
        'user_account':     replace_plain_ids_user_account(user_account),
        'pig_farm_account': farm_account
    }
    
    
    time_final  = time.time()
    delta_secs  = time_final - time_init
    s_time      = '%.2f' % delta_secs
    
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS'
        },
        
        'data': data
    }
    

@app.post("/pig_farm/data")
async def pig_farm_data_post(request: Request, user_data: dm.DataUserLogin):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        # redirect to PAGE_NOT_FOUND
        raise HTTPException(status_code=401, detail="Invalid token")
        
    user_id = res[0]
    
    pig_farm_data = get_farm_data(user_id)
    
    
    # Get browser info 
    browser_info                = get_browser_info(request)
    
    user_data.is_mobile         = 1 if browser_info['is_mobile'] else 0
    user_data.is_webview        = 1 if browser_info['is_webview'] else 0
    user_data.browser           = browser_info['browser']
    user_data.browser_version   = browser_info['browser_version']
    user_data.webview_platform  = browser_info['webview_platform']
    
    user_data.os                = browser_info['os']
    user_data.os_version        = browser_info['os_version']
    user_data.device            = browser_info['device']
    user_data.device_type       = browser_info['device_type'] 
    user_data.ip_address        = browser_info['ip_address']
    
    
    # Update user_login
    model['user'].update_login(user_id, user_data)
    
    
    return pig_farm_data
    


@app.get("/", response_class = HTMLResponse, dependencies=[Depends(public_limit)])
async def root(request: Request, p:str = None):
    """
    2026-01-09 Notes:
    
    
    1.) An account can have several users. 
        The user who registered the account is always admin.
        There can be more than 1 admin user in an account.
        
        Non admin users cannot see billing info.
        
    2.) Company Internal users
        These users are connected to the company. 
        They are connected to a special company account 
        but the company account has no pig farm.
        These users can READ ONLY any account 
        but cannot write any data to the account.  
    
    
    
    In Normal case the user is read from token
    
    Handle all routes:
    - "/" is the ONLY valid route for now (shows home or dashboard based on auth)
    - Any other path redirects to "/" (users should navigate by clicking, not typing)
    
    Parameters
    ----------
    p : str
        pig farm hid;  if this is given, will decode pig_farm_id
        

    """
    
    """
    # If there's any path other than empty string, redirect to home
    if full_path and full_path != "":
        # Optional: Log invalid path attempts for analytics
        print(f"Invalid path attempted: {full_path} - redirecting to home")
        return RedirectResponse(url="/", status_code=302)
    """
    
    
    result = get_current_uhid(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    uhid = result
    
    page = controller.view['root'].render(uhid)
    
    return page
    
    
    
@app.get("/{full_path:path}", response_class=HTMLResponse, dependencies=[Depends(strict_limit)])
async def catch_all_frontend(request: Request, full_path: str = None):
    """
    This catches any route not matched above and serves the frontend
    """
    
    result = get_current_uhid(request)
    if isinstance(result, RedirectResponse):
        return result
    
    uhid = result
    page = controller.view['root'].render(uhid)
    return page
