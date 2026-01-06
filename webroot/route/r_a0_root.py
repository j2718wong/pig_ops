# January 5, 2026
# Jack Wong

import os
import sys
import time

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


from r_utils                import (get_user_account_info,
                                    clean_data_user_account)
from r_pig_production       import get_farm_account_pig_prod_page_data


PIG_FARM_ADD_RES_NUM_SUCCESS        = 0

COMBINED_LACTATING_PIG_OPS  = (PIG_OPERATION_TYPE_LACTATING_PIGLETS, 
                                PIG_OPERATION_TYPE_LACTATING_SOW)


def get_application_data():
    return {
        "product_name":     "PiggyProd",
        "contact_whatsapp": "+85260615575",
        "contact_email":    "support@piggyprod.jsysdev.com"
    }



@app.get("/", response_class = HTMLResponse)
async def root(pfhid:str = None):
    """
    Parameters
    ----------
    pfhid : str
        pig farm hid;  if this is given, wll decode pig_farm_id
    """
    
    time_init = time.time()
    
    
    data_app = get_application_data()
    
    
    # Get the current logged in user;
    # If not logged in, redirect to HOME_PAGE_USER_NOT_LOGGED_IN
    
    
    # At this point user must be logged in
    # temporary
    user_id = 1
    
    user_account = get_user_account_info(user_id)
    
    
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
    

    
    farm_account = get_farm_account_pig_prod_page_data(
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
    
    
    
    