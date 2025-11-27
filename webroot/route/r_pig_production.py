# August 17, 2025
# Jack Wong

import os
import sys
import json
import pprint

from pydantic               import BaseModel

from datetime               import datetime, timedelta

    
sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import data_model           as dm


from r_account              import get_account_lookup_selection


PIG_FARM_ADD_RES_NUM_SUCCESS        = 0


@app.get("/pig_prod_status/list")
async def pig_prod_status_list():
    """
    Will get pig_production status list.
    
    Parameters
    ----------

    """
    
    res = model['pig_prod'].get_pig_prod_status_list()
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
        
        
    for cur_entry in res:
        cur_id  = cur_entry['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res
    }
    


@app.get("/pig_prod"):
async def pig_prod(pfhid:str = None):
    # Get the current logged in user;
    
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
    
    res_user = model['user'].get_user_info(user_id)
    if res_user == None:
        # TODO what to do in case no result
        return None
        
        
    # Get user.account_id 
    account_id = res_user['user']['account_id']
    
    # Get account info
    data_account = model['account'].get_info(account_id)
    if data_account == None:
        # TODO what to do in case no result
        return None
        
        
    # TODO Check account free trial period
        
    # TODO check account for not paid bill
    
        
    # Check if there is a farm_id list
    len_items = len(data_account.farm_ids)
    if len_items = 0:
        # TODO what to do in case no farm set
        return None
        
    if pig_farm_id is not None:
        # This is given by user 
        
        if pig_farm_id not in data_account.farm_ids:
            # TODO what to do in case farm_id given is not in account list
            return None
    
    else:
        # select the first farm_id
        pig_farm_id = data_account.farm_ids[0]
        
    
    # Get account lookup_selection
    list_acc_lookup = get_account_lookup_selection(account_id)
    if list_acc_lookup == None:
        # TODO what to do in case no result
        return None
        
    
    # Get account gestating ops
    list_acc_gestating_ops =  model['account_pig_ops'].get_list(account_id, 
        PIG_OPERATION_TYPE_GESTATING, 0, 0)
    if list_acc_gestating_ops == None:
        # TODO what to do in case no result
        return None
    
    
    # Get account lactating piglets ops
    list_acc_lactating_piglets_ops =  model['account_pig_ops'].get_list(
        account_id, PIG_OPERATION_TYPE_LACTATING_PIGLETS, 0, 0)
    if list_acc_lactating_piglets_ops == None:
        # TODO what to do in case no result
        return None
        
        
    # Get account lactating sow ops
    list_acc_lactating_sow_ops =  model['account_pig_ops'].get_list(
        account_id, PIG_OPERATION_TYPE_LACTATING_SOW, 0, 0)
    if list_acc_lactating_sow_ops == None:
        # TODO what to do in case no result
        return None
    
    
    # Get pig_farm sow list
    list_sow_list = model['sow_boar'].get_list(pig_farm_id, 'F', 
        inc_disposed = 0, inc_external = 0, inc_user_audit = 0, order_by = 0)
    if list_sow_list == None:
        # TODO what to do in case no result
        return None
    
    
    # Get pig_farm boar list
    list_boar_list = model['sow_boar'].get_list(pig_farm_id, 'M', 
        inc_disposed = 0, inc_external = 1, inc_user_audit = 0, order_by = 0)
    if list_boar_list == None:
        # TODO what to do in case no result
        return None
    
    
    # Get semen_source list
    list_semen_source = model['semen_source'].get_list(account_id)
    if list_semen_source == None:
        # TODO what to do in case no result
        return None
        
    
    # Get farm_staff list
    list_staff = model['staff'].get_list(pig_farm_id)
    if list_staff == None:
        # TODO what to do in case no result
        return None
        
    
    # Get feed_type list
    list_feed_type = model['feed_type'].get_list()
    if list_feed_type == None:
        # TODO what to do in case no result
        return None
    
    # Replace feed_type plain id
    for cur_entry in list_feed_type:
        cur_id  = cur_entry['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
    
    
    
    list_feed_brand = model['feed_brand'].get_list(country_id = 1)
    if list_feed_brand == None:
        # TODO what to do in case no result
        return None
    
    # Replace feed_brand plain id
    for cur_entry in list_feed_brand:
        cur_id  = cur_entry['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
    
    
    # Get pig_production list
    
    list_pig_prod = get_pig_prod_list(pig_farm_id)
    if list_feed_brand == None:
        # TODO what to do in case no result
        return None
        
        
    page_data = {
        'account':                  data_account,
        'acc_lookup_selection':		list_acc_lookup,
        'acc_gestating_ops':        list_acc_gestating_ops,
        'acc_lactating_piglets_ops': list_acc_lactating_piglets_ops,
        'acc_lactating_sow_ops':    list_acc_lactating_sow_ops,
        
        'sow_list':                 list_sow_list,
        'boar_list':                list_boar_list,
        'semen_source_list':        list_semen_source,
        'staff_list':               list_staff,
        'feed_type_list':			list_feed_type,
        'feed_brand_list':			list_feed_brand,
        
        'pig_production':           list_pig_prod
    }
    

    return controller.view['pig_prod'].render(page_data = json.dumps(page_data, indent=4))
    
    
    

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
    
    
@app.post("/pig_prod/update_status")
async def pig_prod_update_status(prod_status_data: dm.DataPigProdStatus):
    uhid    = prod_status_data.uhid
    
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
    

    pig_prod_hid    = prod_status_data.pig_prod_hid
    
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


    prod_status_hid = prod_status_data.prod_status_hid
        
    res = hashids_common.decrypt(prod_status_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_PROD_STATUS_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_PROD_STATUS_HASHID',
                'desc': ''
            }
        }
    
    prod_status_id = res[0]
    
    

    prod_status_data.user_id           = user_id
    prod_status_data.pig_prod_id       = pig_prod_id
    prod_status_data.prod_status_id    = prod_status_id
    
    res_update    =  model['pig_prod'].update_status(prod_status_data)
    
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
    res = get_pig_prod_list(pig_farm_id)
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        res 
    }
    
    
def get_pig_prod_list(pig_farm_id):
    res = model['pig_prod'].get_list(pig_farm_id)
    
    
    for cur_entry in res:
        pig_prod_id     = cur_entry['pig_production']['id']
        operation_type  = PIG_OPERATION_TYPE_GESTATING
        
        gestating_ops = model['pig_prod_pig_ops'].get_list(pig_prod_id, 
            operation_type, inc_user_audit = 1)
        
        # Replace plain_id
        
        cur_id  = cur_entry['birth']['birth_staff_id']
        if cur_id is not None:
            cur_hid = hashids_common.encrypt(cur_id)
        else:
            cur_hid = None
        
        del cur_entry['birth']['birth_staff_id']
        cur_entry['birth']['birth_staff_hid']   = cur_hid
            
        
        
        for cur_ops in gestating_ops:
            cur_id  = cur_ops['pig_prod_pig_ops']['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_ops['pig_prod_pig_ops']['id']
            cur_ops['pig_prod_pig_ops']['hid']   = cur_hid
            
            
            cur_id  = cur_ops['account_pig_ops']['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_ops['account_pig_ops']['id']
            cur_ops['account_pig_ops']['hid']   = cur_hid
            
            
            cur_id  = cur_ops['staff']['id']
            if cur_id is not None:
                cur_hid = hashids_common.encrypt(cur_id)
            else:
                cur_hid = None
            
            del cur_ops['staff']['id']
            cur_ops['staff']['hid']   = cur_hid
            
            
            cur_id  = cur_ops['notes']['id']
            if cur_id is not None:
                cur_hid = hashids_common.encrypt(cur_id)
            else:
                cur_hid = None
            
            del cur_ops['notes']['id']
            cur_ops['notes']['hid']   = cur_hid
            
            
        
        cur_entry['gestating_ops'] = gestating_ops
        
    
        operation_type  = PIG_OPERATION_TYPE_LACTATING_PIGLETS
        lactating_piglets_ops = model['pig_prod_pig_ops'].get_list(pig_prod_id, 
            operation_type, inc_user_audit = 1)
        
        for cur_ops in lactating_piglets_ops:
            cur_id  = cur_ops['pig_prod_pig_ops']['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_ops['pig_prod_pig_ops']['id']
            cur_ops['pig_prod_pig_ops']['hid']   = cur_hid
            
            
            cur_id  = cur_ops['account_pig_ops']['id']
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_ops['account_pig_ops']['id']
            cur_ops['account_pig_ops']['hid']   = cur_hid
        
        cur_entry['lactating_piglets_ops'] = lactating_piglets_ops
        
        
        # Replace plain_id
        
        cur_id  = pig_prod_id
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_production']['id']
        cur_entry['pig_production']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['sow']['id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['sow']['id']
        cur_entry['sow']['hid']   = cur_hid
        
        
        # If boar_id is None, delete whole boar block
        cur_id  = cur_entry['insemination']['boar']['id']
        if cur_id is None:
            del cur_entry['insemination']['boar']
        else:
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['insemination']['boar']['id']
            cur_entry['insemination']['boar']['hid']   = cur_hid
    
    
        # If semen_source_id is None, delete whole semen_source block
        cur_id  = cur_entry['insemination']['semen_source']['id']
        if cur_id is None:
            del cur_entry['insemination']['semen_source']
        else:
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['insemination']['semen_source']['id']
            cur_entry['insemination']['semen_source']['hid']   = cur_hid
        
        
        cur_id  = cur_entry['insemination']['insem_staff_id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['insemination']['insem_staff_id']
        cur_entry['insemination']['insem_staff_hid']   = cur_hid
        
        
        # This can be None 
        cur_id  = cur_entry['birth']['birth_staff_id']
        if cur_id is not None: 
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['birth']['birth_staff_id']
            cur_entry['birth']['birth_staff_hid']   = cur_hid
        
    return res


