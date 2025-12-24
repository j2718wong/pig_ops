# August 23, 2025
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import data_model           as dm

   
@app.post("/public_report/add")
async def public_report_add(public_report_data: dm.DataPublicReport):
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_public_report_INVALID_USER_HASHID,
                'code': 'ERROR_public_report_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    supplier_hid    = public_report_data.supplier_hid
    
    res = hashids_common.decrypt(supplier_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BUY_INVALID_FEED_BRAND_HASHID,
                'code': 'ERROR_FEED_BUY_INVALID_FEED_BRAND_HASHID',
                'desc': ''
            }
        }
    
    supplier_id = res[0]
    
    
    
    public_report_data.user_id      = user_id
    public_report_data.supplier_id  = supplier_id
    
    
    res_add    =  model['public_report'].add(public_report_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    
    public_report_id    = res_add['public_report']['id']
    public_report_hid   = hashids_common.encrypt(public_report_id)
    
    # remove plain id
    del res_add['public_report']['id']
    res_add['public_report']['hid'] = public_report_hid

        
    return res_add
    
