# August 17, 2025
# Jack Wong

import os
import sys
import pprint

from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import data_model           as dm


PIG_FARM_ADD_RES_NUM_SUCCESS        = 0


@app.get("/pig_prod_status/list")
async def pig_prod_status_list():
    """
    Will get pig_production status list.
    
    Parameters
    ----------

    """
    
    return model['pig_prod'].get_production_status_list()
    

@app.post("/pig_prod/add")
async def pig_prod_add(pig_farm_data: dm.DataPigFarm):
    name    = pig_farm_data.name
    uhid    = pig_farm_data.uhid
    
    name    = name.strip() if name else None 
    
    if name is None or len(name) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_NAME,
                'code': 'ERROR_PIG_FARM_INVALID_NAME',
                'desc': ''
            }
        }
        
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    pig_farm_data.name      = name
    pig_farm_data.user_id   = user_id
    
    res_add    =  model['pig_farm'].add(pig_farm_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    pig_farm_id     = res_add['pig_farm']['id']
    pig_farm_flag   = res_add['pig_farm']['flag']
        
    pig_farm_hashid = hashids_common.encrypt(pig_farm_id)
    
    if pig_farm_id == 0:
        pig_farm_hashid = ''
    
    # remove plain id
    del res_add['pig_farm']['id']
    res_add['pig_farm']['hid'] = pig_farm_hashid

    result_num      = res_add['result']['num']
    
    if result_num == PIG_FARM_ADD_RES_NUM_SUCCESS:
        data = {
           'pig_farm_id':   pig_farm_id,
           'hashid':        pig_farm_hashid
        }
        res_update = model['pig_farm'].update_hashid(data)
        
    return res_add
    
    

