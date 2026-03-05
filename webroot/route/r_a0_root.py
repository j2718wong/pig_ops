# January 5, 2026
# Jack Wong

import os
import sys
import time
import pprint


import jwt

from fastapi                import Request, HTTPException, status
from pydantic               import BaseModel
from fastapi.responses      import HTMLResponse

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


from r_utils                import replace_plain_ids_user_account


from r_a0_security_checks   import get_user_account_info

from r_pig_production       import get_page_data_farm_account_pig_prod


PIG_FARM_ADD_RES_NUM_SUCCESS        = 0

COMBINED_LACTATING_PIG_OPS  = (PIG_OPERATION_TYPE_LACTATING_PIGLETS, 
                                PIG_OPERATION_TYPE_LACTATING_SOW)


def get_application_data():
    return {
        "product_name":     "SuperPig",
        "contact_whatsapp": "+85260615575",
        "contact_email":    "support@superpig.jsysdev.com",
        
        "rt_updates_enabled": 0
    }


@app.get("/signup", response_class = HTMLResponse)
async def signup():
    page_data = {}
    
    
    #generate_csrf_token() 
    
    page = controller.view['signup'].render(page_data = json.dumps(page_data, indent=4))
    
    return page
    


@app.get("/login", response_class = HTMLResponse)
async def signup():
    page_data = {}
    
    
    #generate_csrf_token() 
    
    page = controller.view['signup'].render(page_data = json.dumps(page_data, indent=4))
    
    return page
    



@app.get("/", response_class = HTMLResponse)
async def root(request: Request, p:str = None):
    """
    2026-01-09 Notes:
    
    
    1.) An account can have several users. 
        The user who registered the account is always admin.
        There can be more than 1 admin user in an account.
        
        Non admin users cannot see billing info.
        
    2.) Company  users
        These users are connected to the company. 
        They are connected to a special company account 
        but the company account has no pig farm.
        These users can READ ONLY any account 
        but cannot write any data to the account.  
    
    
    
    In Normal case the user is read from token
    
    
    Parameters
    ----------
    p : str
        pig farm hid;  if this is given, will decode pig_farm_id
        

    """
    
    token = request.headers.get("authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    
    uhid = None
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        uhid = payload.get("uhid")
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if uhid is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    
    
    time_init = time.time()
    
    
    
    
    
    data_app = get_application_data()
    
    
    # Get the current logged in user;
    # This should be read from a token
    # If not logged in, redirect to HOME_PAGE_USER_NOT_LOGGED_IN
    
    user_id = 0
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        # redirect to PAGE_NOT_FOUND
        raise HTTPException(status_code=401, detail="Invalid token")


        
    user_id = res[0]
    
    
    user_account = get_user_account_info(user_id)
    
    account = user_account['account']
    user    = user_account['user']
    
    print('\n\nroot user account')
    pprint.pprint(user_account)
    
    
    pig_farm_id = None
    
    if p is not None:
        res = hashids_common.decrypt(p)
        if len(res) == 0:
            # Just proceed if it is invalid; will get default 
            # account farm_id if not given
            test = 1
            
            """
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID',
                    'desc': ''
                }
            }
            """
        else:
            pig_farm_id = res[0]
    
    else:
        # Get use user assigned farm id
        # This is the first pig_farm id in user.pig_farms
        user_pig_farms =  user['pig_farms']
        
        if len(user_pig_farms) > 0:
            pig_farm_id = user_pig_farms[0]
    

    
    farm_account = get_page_data_farm_account_pig_prod(
        pig_farm_id, inc_pig_prod = 0, inc_user_audit = 1)
    
    page_data = {}
    page_data['application'] = data_app
    page_data['user_account'] = replace_plain_ids_user_account(user_account)
    page_data['pig_farm_account'] = farm_account  



    time_final  = time.time()
    delta_secs  = time_final - time_init
    s_time      = '%.2f' % delta_secs
    
    print('\n\nroot page_data time(secs): %s' %s_time)
    page = controller.view['root'].render(page_data = json.dumps(page_data, indent=4))
    
    return page
    
    
    
    
