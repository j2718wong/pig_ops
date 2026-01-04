# January 5, 2026
# Jack Wong

import os
import sys

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


from r_pig_production       import get_user_account_pig_prod_page_data


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
    
    
    data_app = get_application_data()
    
    
    # Get the current logged in user;
    # If not logged in, redirect to HOME_PAGE_USER_NOT_LOGGED_IN
    
    
    # At this point user must be logged in
    
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
    
    
    # temporary
    user_id = 1
    
    
    page_data = get_user_account_pig_prod_page_data(user_id, pig_farm_id)
    page_data['application'] = data_app

    page = controller.view['root'].render(page_data = json.dumps(page_data, indent=4))
    
    return page
    
    
    
    