# January 5, 2026
# Jack Wong

import os
import sys
import time
import pprint

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



from r_a0_security_checks   import get_user_account_info

from r_utils                import clean_data_user_account

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
async def root(pfhid:str = None):
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
    
    
    
    Parameters
    ----------
    pfhid : str
        pig farm hid;  if this is given, wll decode pig_farm_id
    """
    
    time_init = time.time()
    
    
    
    
    
    data_app = get_application_data()
    
    
    # Get the current logged in user;
    # If not logged in, redirect to HOME_PAGE_USER_NOT_LOGGED_IN
    
    if pfhid is not None:
        test = 1
    
    # At this point user must be logged in
    # temporary
    user_id = 1
    
    user_account = get_user_account_info(user_id)
    
    account = user_account['account']
  
    
    
    
    pig_farm_id = None
    
    if pfhid is not None:
        res = hashids_common.decrypt(pfhid)
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
        pig_farm_id = 1
    

    
    farm_account = get_page_data_farm_account_pig_prod(
        pig_farm_id, inc_pig_prod = 0, inc_user_audit = 1)
    
    page_data = {}
    page_data['application'] = data_app
    page_data['user_account'] = clean_data_user_account(user_account)
    page_data['pig_farm_account'] = farm_account  



    time_final  = time.time()
    delta_secs  = time_final - time_init
    s_time      = '%.2f' % delta_secs
    
    print('\n\nroot page_data time(secs): %s' %s_time)
    page = controller.view['root'].render(page_data = json.dumps(page_data, indent=4))
    
    return page
    
    
    
    
