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
    
    return model['pig_prod'].get_pig_prod_status_list()
    

@app.post("/pig_prod/add")
async def pig_prod_add(pig_prod_data: dm.DataPigProd):
    uhid    = pig_prod_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    

    sow_hid    = pig_prod_data.sow_hid
    
    res = hashids_common.decrypt(sow_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_SOW_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_SOW_HASHID',
                'desc': ''
            }
        }
    
    sow_id = res[0]
    
    
    boar_hid        = pig_prod_data.boar_hid
    boar_id         = None
    semen_source_id = None
    
    if boar_hid is not None:
        
        res = hashids_common.decrypt(boar_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_BOAR_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_BOAR_HASHID',
                    'desc': ''
                }
            }
        
        boar_id = res[0]
        
    
    else:
        
        semen_source_hid = pig_prod_data.semen_source_hid
        
        res = hashids_common.decrypt(semen_source_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_SEMEN_SOURCE_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_SEMEN_SOURCE_HASHID',
                    'desc': ''
                }
            }
        
        semen_source_id = res[0]
        
    
    insem_staff_hid = pig_prod_data.insem_staff_hid
    insem_staff_id  = None
    
    if insem_staff_hid is not None:
        
        res = hashids_common.decrypt(insem_staff_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_INSEM_STAFF_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_INSEM_STAFF_HASHID',
                    'desc': ''
                }
            }
        
        insem_staff_id = res[0]
    
    

    pig_prod_data.user_id           = user_id
    pig_prod_data.sow_id            = sow_id
    pig_prod_data.boar_id           = boar_id
    pig_prod_data.semen_source_id   = semen_source_id
    pig_prod_data.insem_staff_id    = insem_staff_id
    
    
    res_add    =  model['pig_prod'].add(pig_prod_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    pig_prod_id     = res_add['pig_prod']['id']        
    pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
    
   
    # remove plain id
    del res_add['pig_prod']['id']
    res_add['pig_prod']['hid'] = pig_prod_hashid

    
    pig_prod_ai_id = res_add['pig_prod_ai']['id']
    if pig_prod_ai_id > 0:
        pig_prod_ai_hashid = hashids_common.encrypt(pig_prod_ai_id)
        res_add['pig_prod_ai']['hid'] = pig_prod_ai_hashid
    else:
        del res_add['pig_prod_ai']
  
  
    return res_add
    

@app.post("/pig_prod/fattening/add")
async def pig_prod_fattening_add(pig_fattening_data: dm.DataPigProdFattening):
    uhid    = pig_fattening_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    

    pig_farm_hid = pig_fattening_data.pig_farm_hid
    
        
    res = hashids_common.decrypt(insem_staff_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_INSEM_STAFF_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_INSEM_STAFF_HASHID',
                'desc': ''
            }
        }
    
    pig_farm_id = res[0]

    
    pig_fattening_data.user_id           = user_id
    pig_fattening_data.pig_farm_id       = pig_farm_id
    
    
    
    res_add    =  model['pig_prod'].add_fattening(pig_fattening_data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    pig_prod_id     = res_add['pig_prod']['id']        
    pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
    
   
    # remove plain id
    del res_add['pig_prod']['id']
    res_add['pig_prod']['hid'] = pig_prod_hashid

    return res_add


@app.post("/pig_prod/update_insem")
async def pig_prod_update_insem(pig_prod_data: dm.DataPigProd):
    uhid    = pig_prod_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    

    pig_prod_hid    = pig_prod_data.pig_prod_hid
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_HASHID',
                'desc': ''
            }
        }
    
    pig_prod_id = res[0]


    insem_staff_hid = pig_prod_data.insem_staff_hid
        
    res = hashids_common.decrypt(insem_staff_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_INSEM_STAFF_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_INSEM_STAFF_HASHID',
                'desc': ''
            }
        }
    
    insem_staff_id = res[0]
    
    

    pig_prod_data.user_id           = user_id
    pig_prod_data.pig_prod_id       = pig_prod_id
    pig_prod_data.insem_staff_id    = insem_staff_id
    
    res_update    =  model['pig_prod'].update_insemination(pig_prod_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    pig_prod_id     = res_update['pig_prod']['id']        
    pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
    
   
    # remove plain id
    del res_update['pig_prod']['id']
    res_update['pig_prod']['hid'] = pig_prod_hashid


    return res_update
    
    
@app.post("/pig_prod/update_birth")
async def pig_prod_update_birth(pig_birth_data: dm.DataPigProdBirth):
    uhid    = pig_birth_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    

    pig_prod_hid    = pig_birth_data.pig_prod_hid
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_HASHID',
                'desc': ''
            }
        }
    
    pig_prod_id = res[0]
    
    
    birth_staff_hid = pig_birth_data.birth_staff_hid
        
    res = hashids_common.decrypt(birth_staff_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_BIRTH_STAFF_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_BIRTH_STAFF_HASHID',
                'desc': ''
            }
        }
    
    birth_staff_id = res[0]

    
    
    pig_birth_data.user_id          = user_id
    pig_birth_data.pig_prod_id      = pig_prod_id
    pig_birth_data.birth_staff_id   = birth_staff_id
    
    res_update    =  model['pig_prod'].update_birth(pig_birth_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    pig_prod_id     = res_update['pig_prod']['id']
    pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
    
   
    # remove plain id
    del res_update['pig_prod']['id']
    res_update['pig_prod']['hid'] = pig_prod_hashid


    return res_update
    
    
@app.post("/pig_prod/update_weaning")
async def pig_prod_update_weaning(pig_weaning_data: dm.DataPigProdWeaning):
    uhid    = pig_weaning_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    

    pig_prod_hid    = pig_weaning_data.pig_prod_hid
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_HASHID',
                'desc': ''
            }
        }
    
    pig_prod_id = res[0]
    
   
    
    pig_weaning_data.user_id          = user_id
    pig_weaning_data.pig_prod_id      = pig_prod_id
    
    
    res_update    =  model['pig_prod'].update_weaning(pig_weaning_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    pig_prod_id     = res_update['pig_prod']['id']        
    pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
    
   
    # remove plain id
    del res_update['pig_prod']['id']
    res_update['pig_prod']['hid'] = pig_prod_hashid


    return res_update
    

@app.post("/pig_prod/update_feed_type")
async def pig_prod_update_feed_type(pig_prod_feed_type_data: dm.DataPigProdFeedType):
    uhid    = pig_prod_feed_type_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    

    pig_prod_hid    = pig_prod_feed_type_data.pig_prod_hid
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_HASHID',
                'desc': ''
            }
        }
    
    pig_prod_id = res[0]
    
    
    feed_type_hid    = pig_prod_feed_type_data.feed_type_hid
    
    res = hashids_common.decrypt(feed_type_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_FEED_TYPE_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_FEED_TYPE_HASHID',
                'desc': ''
            }
        }
    
    feed_type_id = res[0]
    
    
    pig_prod_feed_type_data.user_id         = user_id
    pig_prod_feed_type_data.pig_prod_id     = pig_prod_id
    pig_prod_feed_type_data.feed_type_id    = feed_type_id
    
    res_update    =  model['pig_prod'].update_weaning(pig_weaning_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    pig_prod_id     = res_update['pig_prod']['id']        
    pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
    
   
    # remove plain id
    del res_update['pig_prod']['id']
    res_update['pig_prod']['hid'] = pig_prod_hashid


    return res_update
    

@app.post("/pig_prod/update_pig_count")
async def pig_prod_update_pig_count(pig_count_data: dm.DataPigProdPigCount):
    uhid    = pig_count_data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    

    pig_prod_hid    = pig_count_data.pig_prod_hid
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_HASHID',
                'desc': ''
            }
        }
    
    pig_prod_id = res[0]
    
    
    pig_count_data.user_id         = user_id
    pig_count_data.pig_prod_id     = pig_prod_id
    
    res_update    =  model['pig_prod'].update_pig_count(pig_count_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
   
    # remove plain id
    del res_update['pig_prod']['id']
    res_update['pig_prod']['hid'] = pig_prod_hashid


    return res_update
    



@app.get("/pig_prod/list")
async def pig_prod_list(pfhid):
    """
    Will get pig_production list.
    
    Parameters
    ----------
    
    pfhid:str
        pig_farm hashid


    """
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID',
                'desc': ''
            }
        }
    
    
    pig_farm_id = res[0]
    
    
    
    res = model['pig_prod'].get_list(pig_farm_id)
    
    """
    for cur_entry in res:
        pig_prod_id     = cur_entry['pig_production']['id']
        operation_type  = PIG_OPERATION_TYPE_GESTATING
        
        gestating_ops = model['pig_prod_pig_ops'].get_list(pig_prod_id, 
            operation_type, inc_user_audit = 1)
        
        cur_entry['gestating_ops'] = gestating_ops

    
        operation_type  = PIG_OPERATION_TYPE_LACTATING
        lactating_ops = model['pig_prod_pig_ops'].get_list(pig_prod_id, 
            operation_type, inc_user_audit = 1)
        
        cur_entry['lactating_ops'] = lactating_ops
        
        prod_notes =  model['prod_notes'].get_list(pig_prod_id)
        
        cur_entry['prod_notes'] = prod_notes
    """
    return res


