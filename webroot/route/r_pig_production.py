# August 17, 2025
# Jack Wong

import os
import sys
import json
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


from r_account_selection    import get_account_lookup_selection
from r_utils                import (get_user_account_info,
                                   get_location_address_names_and_replace_ids)


PIG_FARM_ADD_RES_NUM_SUCCESS        = 0

COMBINED_LACTATING_PIG_OPS  = (PIG_OPERATION_TYPE_LACTATING_PIGLETS, 
                                PIG_OPERATION_TYPE_LACTATING_SOW)



def get_user_account_pig_prod_page_data(user_id, pig_farm_id = None,
        inc_pig_prod = 0):
            
    """
    Will get user account pig_prod_page data. 
    This is a large data block getting data from several tables.
    To minimize execution time, it is possible to request 
    the actual pig_prod data later via separate request.
    
    Parameters
    ----------
    user_id : int
    
    pig_farm_id: int
    
    inc_pig_prod : int
        flag to include pig_prod data.
        
    """
            
    user_account    = get_user_account_info(user_id)
    
    data_user       = user_account['user']
    data_account    = user_account['account']
        
    # Check if there are account farms
    
    if 'pig_farms' not in data_account:
        # TODO what to do here
        print('Error 2')
        return None   
    
    
    account_pig_farms = data_account['pig_farms']
    
    print('data_user')
    pprint.pprint(data_user)
    
    print('data_account')
    pprint.pprint(data_account)
    
    len_items = len(account_pig_farms)
    if len_items == 0:
        # TODO what to do in case no farm set
        print('Error 3')
        return None
        
        
    if pig_farm_id is not None:
        # This is given by user; This is possible.
        
        if pig_farm_id not in account_farm_ids:
            # TODO what to do in case farm_id given is not in account list
            print('Error 4')
            return None
    
    else:
        # select the first farm_id
        pig_farm_id = account_pig_farms[0]['pig_farm']['id']
        
    
    account_id = data_account['account']['id']
    
    
def get_farm_account_pig_prod_page_data(pig_farm_id, 
        inc_pig_prod = 0, inc_user_audit = 0):
    
    pig_farm_account= model['pig_farm'].get_pig_farm_account_info(pig_farm_id)
    
    if pig_farm_account == None: return None
    
    account_id = pig_farm_account['account']['id']
    
    pig_prod_page_data  = get_pig_prod_page_data(account_id, pig_farm_id, 
            inc_pig_prod, inc_user_audit = inc_user_audit)
    
    
    # Replace plain id
    cur_id      = account_id
    cur_hid     = hashids_account.encrypt(cur_id)
    
    del pig_farm_account['account']['id']
    pig_farm_account['account']['hid']   = cur_hid

    
    cur_id = pig_farm_account['account_bill']['id']
    if cur_id == 0:
        del pig_farm_account['account_bill']

    else:
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del pig_farm_account['account_bill']['id']
        pig_farm_account['account_bill']['hid']   = cur_hid

    
    pig_prod_page_data['account'] = pig_farm_account
    
    return pig_prod_page_data

    
def get_pig_prod_page_data(account_id, pig_farm_id, inc_pig_prod = 0,
        inc_user_audit = 0, minimum_info = 1):
    
    list_acc_pig_ops =  model['account_pig_ops'].get_list(account_id, None, 
        inc_deleted = 0, inc_user_audit = inc_user_audit)
    if list_acc_pig_ops == None:
        # TODO what to do in case no result
        print('Error 8')
        return None
    

    # Get pig_farm sow list
    list_sow_list = model['sow_boar'].get_list(pig_farm_id, 'F', 
        inc_user_audit = 0, order_by = 1)
    if list_sow_list == None:
        # TODO what to do in case no result
        print('Error 9')
        return None
    
    
    # Get sow production output list
    list_sow_output_list = model['pig_prod'].get_production_output(
        pig_farm_id = pig_farm_id);
    
    
    for cur_sow in list_sow_list:
        cur_sow_id = cur_sow['id']
        
        for cur_sow_output in list_sow_output_list:
            if cur_sow_output['sow_id'] == cur_sow_id:
                cur_sow['num_births'] = cur_sow_output['num_births']
                cur_sow['num_piglets'] = cur_sow_output['num_piglets']
                
                break
    
    
    # Get pig_farm boar list
    list_boar_list = model['sow_boar'].get_list(pig_farm_id, 'M', 
        inc_user_audit = 0, order_by = 1)
    if list_boar_list == None:
        # TODO what to do in case no result
        print('Error 10')
        return None

    
    # Get farm_staff list
    list_staff = model['pig_farm_staff'].get_list(pig_farm_id, 
        minimum_info = minimum_info)
    if list_staff == None:
        # TODO what to do in case no result
        print('Error 12')
        return None
        
    
    list_pig_prod = None
    if inc_pig_prod > 0:
    
        pig_prod_type = PIG_PROD_TYPE['GESTATING']
        
        # Get pig_production list
        list_pig_prod = get_pig_prod_list(pig_farm_id, pig_prod_type)
        if list_pig_prod == None:
            # TODO what to do in case no result
            print('Error 17')
            return None
            


    # Remove plain_ids and not useful data blocks
    
    for cur_entry in list_acc_pig_ops:
        cur_id      = cur_entry['acc_pig_ops']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['acc_pig_ops']['id']
        cur_entry['acc_pig_ops']['hid']   = cur_hid
    
    
    
    for cur_entry in list_sow_list:
        cur_id      = cur_entry['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
        
        
        cur_id      = cur_entry['last_mate_sow_boar_id']
        if cur_id is not None:
            cur_hid     = hashids_common.encrypt(cur_id)
        else:
            cur_hid = None
            
        del cur_entry['last_mate_sow_boar_id']
        cur_entry['last_mate_sow_boar_hid']   = cur_hid
        
    
    for cur_entry in list_boar_list:
        cur_id      = cur_entry['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
    
    
        cur_id      = cur_entry['last_mate_sow_boar_id']
        if cur_id is not None:
            cur_hid     = hashids_common.encrypt(cur_id)
        else:
            cur_hid = None
            
        del cur_entry['last_mate_sow_boar_id']
        cur_entry['last_mate_sow_boar_hid']   = cur_hid
        

        
    for cur_entry in list_staff:
        cur_id      = cur_entry['pig_farm_staff']['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['pig_farm_staff']['id']
        cur_entry['pig_farm_staff']['hid']   = cur_hid
        


    pig_farm_account = {
        'acc_pig_ops':              list_acc_pig_ops,
        
        'sow_list':                 list_sow_list,
        'boar_list':                list_boar_list,
        'staff_list':               list_staff
        
    }
    
    if inc_pig_prod > 0:
        pig_farm_account['pig_production']  = list_pig_prod
    
    return pig_farm_account


@app.get("/pig_prod", response_class = HTMLResponse, tags=["Pig Production"])
async def pig_prod(pfhid:str = None, m:int =0):
    """
    Parameters
    ----------
    m : int
        temporary distinction to request from mobile page.
        if == 0, request for web version
        if > 0, request for mobile version
    """
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
            
    else:
        pig_farm_id = 1 # temporary
    
    
    t0 = time.time()
    
    page_data = get_farm_account_pig_prod_page_data(pig_farm_id, inc_pig_prod = 1)

    t1 = time.time()
    
    page = controller.view['pig_prod'].render(page_data = json.dumps(page_data, indent=4),
        is_mobile = m)
    
    t2 = time.time()
    
    
    delta_t1 = t1 - t0
    delta_t2 = t2 - t1
    
    delta_t  = t2 - t0
    
    s_delta_t1      = '%.2f' % delta_t1
    s_delta_t2      = '%.2f' % delta_t2
    s_delta_t       = '%.2f' % delta_t
    
    
    
    print('\n\npig_prod page_data time(secs): %s' %s_delta_t)
    print('getting  page_data time(secs): %s' %s_delta_t1)
    print('rendering page_data time(secs): %s' %s_delta_t2)
    
    return page
    


@app.get("/pig_fattening", response_class = HTMLResponse, tags=["Pig Production"])
async def pig_fattening(pfhid:str = None):
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
    account_farm_ids = data_account['farm_ids']
    len_items = len(account_farm_ids)
    if len_items == 0:
        # TODO what to do in case no farm set
        return None
        
    if pig_farm_id is not None:
        # This is given by user 
        
        if pig_farm_id not in account_farm_ids:
            # TODO what to do in case farm_id given is not in account list
            return None
    
    else:
        # select the first farm_id
        pig_farm_id = account_farm_ids[0]
        
        
        
        
    page_data = {
        'account':                  data_account,
                
        'staff_list':               list_staff,
        'feed_type_list':           list_feed_type,
        'feed_brand_list':          list_feed_brand,
        'feed_supplier_list':       list_feed_supplier,
        
        'pig_production':           list_pig_prod
    }
    

    page = controller.view['pig_prod'].render(page_data = json.dumps(page_data, indent=4))
    
    return page
    


@app.get("/pig_prod_status/list", tags=["Pig Production"])
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
    

@app.get("/pig_prod/public", tags=["Pig Production"])
async def pig_prod_public(country_hid:str):
    """
    Will get pig_production public data.
    
    Parameters
    ----------

    """
    
    country_id = 0
    
            
    res = hashids_common.decrypt(country_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_ADDRESS_COUNTRY_HID,
                'code': 'ERROR_ADDRESS_COUNTRY_HID',
                'desc': ''
            }
        }
    
    country_id = res[0]

    
    
    # Get feed_type list
    # This is the same data for all accounts
    list_feed_type = model['feed_type'].get_list()
    if list_feed_type == None:
        # TODO what to do in case no result
        print('Error 13')
        return None
    
    
    # Get feed_brand list
    # This is the same for all accounts by country_id
    list_feed_brand = model['feed_brand'].get_list(country_id = country_id)
    if list_feed_brand == None:
        # TODO what to do in case no result
        print('Error 14')
        return None
    

    # Get pig_dead_type list
    # This is the same for all accounts
    list_pig_dead_type = model['prod_pig_dead'].get_pig_dead_type_list()
    if list_pig_dead_type == None:
        # TODO what to do in case no result
        print('Error 16')
        return None

    
    
    
    for cur_entry in list_feed_type:
        cur_id      = cur_entry['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
    

    for cur_entry in list_feed_brand:
        cur_id      = cur_entry['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
    
    
    for cur_entry in list_pig_dead_type:
        cur_id      = cur_entry['id']
        cur_hid     = hashids_common.encrypt(cur_id)
        
        del cur_entry['id']
        cur_entry['hid']   = cur_hid
    
    return {
        
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
    
        'data': {
            'feed_type_list':           list_feed_type,
            'feed_brand_list':          list_feed_brand,
            'pig_dead_type_list':       list_pig_dead_type
        }
    }
    
    

@app.post("/pig_prod/add", tags=["Pig Production"])
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
    
    
    boar_id             = None
    semen_supplier_id   = None
    semen_sup_semen_id  = None
    semen_ai_boar_id    = None
    
    
    boar_hid        = pig_prod_data.boar_hid
    
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
        
        semen_supplier_hid = pig_prod_data.semen_supplier_hid
        
        res = hashids_common.decrypt(semen_supplier_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_SEMEN_SUPPLIER_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_SEMEN_SUPPLIER_HASHID',
                    'desc': ''
                }
            }
        
        semen_supplier_id = res[0]
        
        
        semen_sup_semen_hid = pig_prod_data.semen_sup_semen_hid
        
        res = hashids_common.decrypt(semen_sup_semen_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_SEMEN_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_SEMEN_HASHID',
                    'desc': ''
                }
            }
        
        semen_sup_semen_id = res[0]
        
        
        semen_ai_boar_hid = pig_prod_data.semen_ai_boar_hid
        
        res = hashids_common.decrypt(semen_ai_boar_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_AI_BOAR_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_AI_BOAR_HASHID',
                    'desc': ''
                }
            }
        
        semen_ai_boar_id = res[0]
        
        
    
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
    pig_prod_data.semen_supplier_id = semen_supplier_id
    pig_prod_data.semen_sup_semen_id = semen_sup_semen_id
    pig_prod_data.semen_ai_boar_id  = semen_ai_boar_id
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
    

@app.post("/pig_prod/fattening/add", tags=["Pig Production"])
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


@app.post("/pig_prod/update_insem", tags=["Pig Production"])
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


    boar_id             = None
    semen_supplier_id   = None
    semen_sup_semen_id  = None
    semen_ai_boar_id    = None
    
    
    boar_hid        = pig_prod_data.boar_hid
    
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
        
        semen_supplier_hid = pig_prod_data.semen_supplier_hid
        
        res = hashids_common.decrypt(semen_supplier_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_SEMEN_SOURCE_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_SEMEN_SOURCE_HASHID',
                    'desc': ''
                }
            }
        
        semen_supplier_id = res[0]
        
        
        semen_sup_semen_hid = pig_prod_data.semen_sup_semen_hid
        
        res = hashids_common.decrypt(semen_sup_semen_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_SEMEN_SOURCE_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_SEMEN_SOURCE_HASHID',
                    'desc': ''
                }
            }
        
        semen_sup_semen_id = res[0]
        
        
        semen_ai_boar_hid = pig_prod_data.semen_ai_boar_hid
        
        res = hashids_common.decrypt(semen_ai_boar_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_SEMEN_SOURCE_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_SEMEN_SOURCE_HASHID',
                    'desc': ''
                }
            }
        
        semen_ai_boar_id = res[0]
    
    
    
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
    pig_prod_data.boar_id           = boar_id
    pig_prod_data.semen_supplier_id   = semen_supplier_id
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
    
    
@app.post("/pig_prod/update_status", tags=["Pig Production"])
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
    
    
@app.post("/pig_prod/update_birth", tags=["Pig Production"])
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
    
    
@app.post("/pig_prod/update_weaning", tags=["Pig Production"])
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
    

@app.post("/pig_prod/update_feed_start_date", tags=["Pig Production"])
async def pig_prod_update_feed_start_date(feed_start_date_data: dm.DataFeedStartDate):
    uhid    = feed_start_date_data.uhid
    
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
    

    pig_prod_hid    = feed_start_date_data.pig_prod_hid
    
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
    
    
    feed_type_hid    = feed_start_date_data.feed_type_hid
    
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
    
    
    feed_start_date_data.user_id         = user_id
    feed_start_date_data.pig_prod_id     = pig_prod_id
    feed_start_date_data.feed_type_id    = feed_type_id
    
    res_update    =  model['pig_prod'].update_feed_start_date(feed_start_date_data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    

    return res_update
    

@app.post("/pig_prod/update_pig_count", tags=["Pig Production"])
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
    


@app.get("/pig_prod/feed_summary", tags=["Pig Production"])
async def pig_prod_feed_summary(pig_prod_hid:str):
    """
    Will get pig_production feed summary by pig_prod_hid.
    
    Parameters
    ----------
    
    pig_prod_hid:str
        pig_production hashid


    """
    
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
    
    res = model['pig_prod'].get_feed_summary_by_id(pig_prod_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res 
    }


@app.get("/pig_prod/cur_pig_count", tags=["Pig Production"])
async def pig_prod_cur_pig_count(pig_prod_hid:str):
    """
    Will get pig_production.num_pigs_current.
    
    This is a dedicated API just to get this column because
    every pig_dead entry or pig_add entry to a pig_production 
    will recompute this number. 
    
    Parameters
    ----------
    
    pig_prod_hid:str
        pig_production hashid


    """
    
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
    
    res = model['pig_prod'].get_cur_pig_count_by_id(pig_prod_id)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR',
                'desc': ''
            }
        }
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res 
    }



@app.get("/pig_prod/list", tags=["Pig Production"])
async def pig_prod_list(pfhid:str, pig_prod_type:int = 0,  is_mob_view:int = 0):
    """
    Will get pig_production list.
    
    Parameters
    ----------
    
    pfhid:str
        pig_farm hashid


    pig_prod_type: int
        combination of flag bits
        
        1 = PROD_TYPE_GESTA
        2 = PROD_TYPE_LACTA
        4 = PROD_TYPE_FATTENING
    


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
    res = get_pig_prod_list(pig_farm_id, pig_prod_type, is_mob_view)
    
    return {
        'result':{
            'num':  0,
            'code': 'SUCCESS',
            'desc': ''
        },
        
        'data': res 
    }
    
    
def get_pig_prod_list(pig_farm_id, pig_prod_type, is_mob_view = 0):
    res = model['pig_prod'].get_list(pig_farm_id, pig_prod_type)
    
    
    for cur_entry in res:
        pig_prod_id     = cur_entry['pig_production']['id']
        
        order_by = 0 if is_mob_view == 0 else 1
        
        operation_type  = PIG_OPERATION_TYPE_GESTATING
        gestating_ops = model['pig_prod_pig_ops'].get_list(pig_prod_id, 
            operation_type, inc_user_audit = 1, order_by = order_by)
        
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
        
        
        # Get Lactating Pig Operations
        # Initially, the piglets and sow pig operations are requested 
        # separately. But in mobile web, this is shown as one list.
        
        if is_mob_view == 0:
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
            
            
            operation_type  = PIG_OPERATION_TYPE_LACTATING_SOW
            lactating_sow_ops = model['pig_prod_pig_ops'].get_list(pig_prod_id, 
                operation_type, inc_user_audit = 1)
            
            for cur_ops in lactating_sow_ops:
                cur_id  = cur_ops['pig_prod_pig_ops']['id']
                cur_hid = hashids_common.encrypt(cur_id)
                
                del cur_ops['pig_prod_pig_ops']['id']
                cur_ops['pig_prod_pig_ops']['hid']   = cur_hid
                
                
                cur_id  = cur_ops['account_pig_ops']['id']
                cur_hid = hashids_common.encrypt(cur_id)
                
                del cur_ops['account_pig_ops']['id']
                cur_ops['account_pig_ops']['hid']   = cur_hid
            
            cur_entry['lactating_sow_ops'] = lactating_sow_ops
        
        else:
            # Combine lactating pig_ops
            
            operation_type  = COMBINED_LACTATING_PIG_OPS
            lactating_ops = model['pig_prod_pig_ops'].get_list(pig_prod_id, 
                operation_type, inc_user_audit = 1, order_by = 1)
            
            for cur_ops in lactating_ops:
                cur_id  = cur_ops['pig_prod_pig_ops']['id']
                cur_hid = hashids_common.encrypt(cur_id)
                
                del cur_ops['pig_prod_pig_ops']['id']
                cur_ops['pig_prod_pig_ops']['hid']   = cur_hid
                
                
                cur_id  = cur_ops['account_pig_ops']['id']
                cur_hid = hashids_common.encrypt(cur_id)
                
                del cur_ops['account_pig_ops']['id']
                cur_ops['account_pig_ops']['hid']   = cur_hid
            
            cur_entry['lactating_ops'] = lactating_ops
            
        
        
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
            
            
            # If semen_supplier_id is None, delete whole semen_supplier block
            cur_id  = cur_entry['insemination']['ai']['semen_supplier']['id']
            if cur_id is None:
                del cur_entry['insemination']['ai']['semen_supplier']
            
                cur_id  = cur_entry['insemination']['ai']['internal_boar']['id']
                if cur_id is None:
                    del cur_entry['insemination']['ai']['internal_boar']
                else:
                    cur_hid = hashids_common.encrypt(cur_id)
                    
                    del cur_entry['insemination']['ai']['internal_boar']['id']
                    cur_entry['insemination']['ai']['internal_boar']['hid'] = cur_hid
            else:
                # encrypt semen_supplier.id
                cur_hid = hashids_common.encrypt(cur_id)
                
                del cur_entry['insemination']['ai']['semen_supplier']['id']
                cur_entry['insemination']['ai']['semen_supplier']['hid']   = cur_hid
                
                # encrypt semen_supplier.semen.id
                cur_id  = cur_entry['insemination']['ai']['semen_supplier']['semen']['id']
                cur_hid = hashids_common.encrypt(cur_id)
                
                del cur_entry['insemination']['ai']['semen_supplier']['semen']['id']
                cur_entry['insemination']['ai']['semen_supplier']['semen']['hid']   = cur_hid
                
                
            
        else:
            cur_hid = hashids_common.encrypt(cur_id)
            
            del cur_entry['insemination']['boar']['id']
            cur_entry['insemination']['boar']['hid']   = cur_hid
            
            
            # delete whole ai block
            del cur_entry['insemination']['ai']
    
    
        
        cur_id  = cur_entry['insemination']['insem_staff_id']
        cur_hid = hashids_common.encrypt(cur_id)
        
        del cur_entry['insemination']['insem_staff_id']
        cur_entry['insemination']['insem_staff_hid']   = cur_hid
        
        
        
    return res


