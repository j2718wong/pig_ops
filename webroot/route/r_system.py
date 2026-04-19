# April 19, 2026
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


from fastapi.responses      import PlainTextResponse


import data_model           as dm


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)


from r_a0_security_checks   import check_if_valid_user_account
from r_utils                import remove_database_null_description


@app.get("/system/stats", tags=["System"])
async def system_stats(request: Request):
    """
    Will get system stats.
    
    Parameters
    ----------
    
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    res = model['system'].get_sys_stats()
    
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
        
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }


@app.get("/system/latest_users", tags=["System"])
async def system_latest_users(request: Request):
    """
    Will get system latest_users.
    
    Parameters
    ----------
    
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    res = model['system'].get_latest_user_list()
    
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
        
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }


