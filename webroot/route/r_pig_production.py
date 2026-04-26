# August 17, 2025
# Jack Wong

import os
import sys
import json
import time
import pprint


from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse


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


from r_a0_security_checks   import check_if_valid_user_account

from r_utils                import remove_database_null_description



@app.post("/pig_prod/add", tags=["Pig Production"])
async def pig_prod_add(request: Request, data: dm.DataPigProd):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    

    sow_hid    = data.sow_hid
    
    res = hashids_common.decrypt(sow_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_SOW_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_SOW_HASHID'
            }
        }
    
    sow_id = res[0]
    
    
    boar_id             = None
    semen_supplier_id   = None
    semen_sup_semen_id  = None
    semen_ai_boar_id    = None
    
    
    boar_hid        = data.boar_hid
    
    if boar_hid is not None:
        
        res = hashids_common.decrypt(boar_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_BOAR_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_BOAR_HASHID'
                }
            }
        
        boar_id = res[0]
        
    
    else:
        
        semen_supplier_hid = data.semen_supplier_hid
        
        if semen_supplier_hid is not None:
            res = hashids_common.decrypt(semen_supplier_hid)
            if len(res) == 0:
            
                return {
                    'result':{
                        'num':  ERROR_PIG_PROD_INVALID_SEMEN_SUPPLIER_HASHID,
                        'code': 'ERROR_PIG_PROD_INVALID_SEMEN_SUPPLIER_HASHID'
                    }
                }
            
            semen_supplier_id = res[0]
        
        
        semen_sup_semen_hid = data.semen_sup_semen_hid
        
        if semen_sup_semen_hid is not None:
            res = hashids_common.decrypt(semen_sup_semen_hid)
            if len(res) == 0:
            
                return {
                    'result':{
                        'num':  ERROR_PIG_PROD_INVALID_SEMEN_HASHID,
                        'code': 'ERROR_PIG_PROD_INVALID_SEMEN_HASHID'
                    }
                }
            
            semen_sup_semen_id = res[0]
        
        
        semen_ai_boar_hid = data.semen_ai_boar_hid
        
        if semen_ai_boar_hid is not None:
            res = hashids_common.decrypt(semen_ai_boar_hid)
            if len(res) == 0:
            
                return {
                    'result':{
                        'num':  ERROR_PIG_PROD_INVALID_AI_BOAR_HASHID,
                        'code': 'ERROR_PIG_PROD_INVALID_AI_BOAR_HASHID'
                    }
                }
            
            semen_ai_boar_id = res[0]
        
        
        # Additional validation
        if semen_ai_boar_id is None:
            if semen_supplier_id is None  or semen_sup_semen_hid is None:
                
                # either semen_supplier or semen_sup_semen is error
                return {
                    'result':{
                        'num':  ERROR_PIG_PROD_INVALID_SEMEN_SUPPLIER_HASHID,
                        'code': 'ERROR_PIG_PROD_INVALID_SEMEN_SUPPLIER_HASHID'
                    }
                }
                
        
    
    insem_staff_hid = data.insem_staff_hid
    insem_staff_id  = None
    
    if insem_staff_hid is not None:
        
        res = hashids_common.decrypt(insem_staff_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_INSEM_STAFF_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_INSEM_STAFF_HASHID'
                }
            }
        
        insem_staff_id = res[0]
    
    

    data.user_id           = user_id
    data.sow_id            = sow_id
    data.boar_id           = boar_id
    data.semen_supplier_id = semen_supplier_id
    data.semen_sup_semen_id = semen_sup_semen_id
    data.semen_ai_boar_id  = semen_ai_boar_id
    data.insem_staff_id    = insem_staff_id
    
    
    res_add    =  model['pig_prod'].add(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    pig_prod_id     = res_add['pig_prod']['id']        
    pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
    
   
    # remove plain id
    del res_add['pig_prod']['id']
    res_add['pig_prod']['hid'] = pig_prod_hashid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)
    
    return res_add
    

@app.post("/pig_prod/fattening/add", tags=["Pig Production"])
async def pig_prod_fattening_add(request: Request, data: dm.DataPigProdNoSow):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    

    pig_farm_hid = data.pig_farm_hid
    
        
    res = hashids_common.decrypt(pig_farm_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_PIG_FARM_HASHID'
            }
        }
    
    pig_farm_id = res[0]

    
    data.user_id           = user_id
    data.pig_farm_id       = pig_farm_id
    
    
    
    res_add    =  model['pig_prod'].add_fattening(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    pig_prod_id     = res_add['pig_prod']['id']        
    pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
    
   
    # remove plain id
    del res_add['pig_prod']['id']
    res_add['pig_prod']['hid'] = pig_prod_hashid
    
    
    # Remove optional desc coming from database
    remove_database_null_description(res_add)
    
    return res_add


#@app.post("/pig_prod/pig_add", tags=["Pig Production"])



@app.post("/pig_prod/update_insem", tags=["Pig Production"])
async def pig_prod_update_insem(request: Request, data: dm.DataPigProd):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    

    pig_prod_hid    = data.pig_prod_hid
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_HASHID'
            }
        }
    
    pig_prod_id = res[0]


    boar_id             = None
    semen_supplier_id   = None
    semen_sup_semen_id  = None
    semen_ai_boar_id    = None
    
    
    boar_hid        = data.boar_hid
    
    if boar_hid is not None:
        
        res = hashids_common.decrypt(boar_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_BOAR_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_BOAR_HASHID'
                }
            }
        
        boar_id = res[0]
        
    
    else:
        
        semen_supplier_hid = data.semen_supplier_hid
        
        if semen_supplier_hid is not None:
            res = hashids_common.decrypt(semen_supplier_hid)
            if len(res) == 0:
            
                return {
                    'result':{
                        'num':  ERROR_PIG_PROD_INVALID_SEMEN_SOURCE_HASHID,
                        'code': 'ERROR_PIG_PROD_INVALID_SEMEN_SOURCE_HASHID'
                    }
                }
            
            semen_supplier_id = res[0]
        
        
        semen_sup_semen_hid = data.semen_sup_semen_hid
        
        if semen_sup_semen_hid is not None:
            res = hashids_common.decrypt(semen_sup_semen_hid)
            if len(res) == 0:
            
                return {
                    'result':{
                        'num':  ERROR_PIG_PROD_INVALID_SEMEN_SOURCE_HASHID,
                        'code': 'ERROR_PIG_PROD_INVALID_SEMEN_SOURCE_HASHID'
                    }
                }
            
            semen_sup_semen_id = res[0]
            
        
        semen_ai_boar_hid = data.semen_ai_boar_hid
        
        if semen_ai_boar_hid is not None:
            res = hashids_common.decrypt(semen_ai_boar_hid)
            if len(res) == 0:
            
                return {
                    'result':{
                        'num':  ERROR_PIG_PROD_INVALID_AI_BOAR_HASHID,
                        'code': 'ERROR_PIG_PROD_INVALID_AI_BOAR_HASHID'
                    }
                }
            
            semen_ai_boar_id = res[0]
        
        
        # Additional validation
        if semen_ai_boar_id is None:
            if semen_supplier_id is None  or semen_sup_semen_hid is None:
                
                # either semen_supplier or semen_sup_semen is error
                return {
                    'result':{
                        'num':  ERROR_PIG_PROD_INVALID_SEMEN_SUPPLIER_HASHID,
                        'code': 'ERROR_PIG_PROD_INVALID_SEMEN_SUPPLIER_HASHID'
                    }
                }
        
    
    insem_staff_hid = data.insem_staff_hid
        
    res = hashids_common.decrypt(insem_staff_hid)
    if len(res) == 0:
    
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_INSEM_STAFF_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_INSEM_STAFF_HASHID'
            }
        }
    
    insem_staff_id = res[0]
    
    

    data.user_id           = user_id
    data.pig_prod_id       = pig_prod_id
    data.boar_id           = boar_id
    data.semen_supplier_id   = semen_supplier_id
    data.semen_sup_semen_id  = semen_sup_semen_id
    data.insem_staff_id    = insem_staff_id
    data.semen_ai_boar_id  = semen_ai_boar_id
    
    res_update    =  model['pig_prod'].update_insemination(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    pig_prod_id     = res_update['pig_prod']['id']        
    pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
    
   
    # remove plain id
    del res_update['pig_prod']['id']
    res_update['pig_prod']['hid'] = pig_prod_hashid

    
    remove_database_null_description(res_update)

    return res_update
    
    
@app.post("/pig_prod/update_status", tags=["Pig Production"])
async def pig_prod_update_status(request: Request, data: dm.DataPigProdStatus):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    

    pig_prod_hid    = data.pig_prod_hid
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_HASHID'
            }
        }
    
    pig_prod_id = res[0]


    data.user_id           = user_id
    data.pig_prod_id       = pig_prod_id

    
    res_update    =  model['pig_prod'].update_status(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    pig_prod_id     = res_update['pig_prod']['id']        
    pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
    
   
    # remove plain id
    del res_update['pig_prod']['id']
    res_update['pig_prod']['hid'] = pig_prod_hashid

    
    # Remove optional desc coming from database
    remove_database_null_description(res_update)

    return res_update
    
    
@app.post("/pig_prod/update_birth", tags=["Pig Production"])
async def pig_prod_update_birth(request: Request, data: dm.DataPigProdBirth):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    


    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    


    pig_prod_hid    = data.pig_prod_hid
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_HASHID'
            }
        }
    
    pig_prod_id = res[0]
    
    
    birth_staff_id  = None
    birth_staff_hid = data.birth_staff_hid
    
    if birth_staff_hid is not None:
        res = hashids_common.decrypt(birth_staff_hid)
        if len(res) == 0:
        
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_BIRTH_STAFF_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_BIRTH_STAFF_HASHID'
                }
            }
        
        birth_staff_id = res[0]

    
    
    data.user_id          = user_id
    data.pig_prod_id      = pig_prod_id
    data.birth_staff_id   = birth_staff_id
    
    res_update    =  model['pig_prod'].update_birth(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    pig_prod_id     = res_update['pig_prod']['id']
    pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
    
   
    # remove plain id
    del res_update['pig_prod']['id']
    res_update['pig_prod']['hid'] = pig_prod_hashid


    # Remove optional desc coming from database
    remove_database_null_description(res_update)

    return res_update
    
    
@app.post("/pig_prod/update_weaning", tags=["Pig Production"])
async def pig_prod_update_weaning(request: Request, data: dm.DataPigProdWeaning):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    


    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    


    pig_prod_hid    = data.pig_prod_hid
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_HASHID'
            }
        }
    
    pig_prod_id = res[0]
    
    
    if data.num_pigs_male is None and data.num_pigs_female is None and data.num_pigs is None:       
        return {
            'result':{
                'num':  ERROR_PIG_PROD_NUM_PIGS_ALL_NONE,
                'code': 'ERROR_PIG_PROD_NUM_PIGS_ALL_NONE'
            }
        }
    
    
    data.user_id          = user_id
    data.pig_prod_id      = pig_prod_id
    
    
    res_update    =  model['pig_prod'].update_weaning(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    pig_prod_id     = res_update['pig_prod']['id']        
    pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
    
   
    # remove plain id
    del res_update['pig_prod']['id']
    res_update['pig_prod']['hid'] = pig_prod_hashid


    # Remove optional desc coming from database
    remove_database_null_description(res_update)

    return res_update
    

@app.post("/pig_prod/update_feed_start_date", tags=["Pig Production"])
async def pig_prod_update_feed_start_date(request: Request, data: dm.DataFeedStartDate):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    

    pig_prod_hid    = data.pig_prod_hid
    
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
    
    
    feed_type_hid    = data.feed_type_hid
    
    res = hashids_common.decrypt(feed_type_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_FEED_TYPE_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_FEED_TYPE_HASHID'
            }
        }
    
    feed_type_id = res[0]
    
    
    data.user_id         = user_id
    data.pig_prod_id     = pig_prod_id
    data.feed_type_id    = feed_type_id
    
    res_update    =  model['pig_prod'].update_feed_start_date(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    

    return res_update
    

@app.post("/pig_prod/update_pig_count", tags=["Pig Production"])
async def pig_prod_update_pig_count(request: Request, data: dm.DataPigProdPigCount):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    #uhid    = data.uhid
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    

    pig_prod_hid    = data.pig_prod_hid
    
    res = hashids_common.decrypt(pig_prod_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_PROD_INVALID_HASHID,
                'code': 'ERROR_PIG_PROD_INVALID_HASHID'
            }
        }
    
    pig_prod_id = res[0]
    
    
    data.user_id         = user_id
    data.pig_prod_id     = pig_prod_id
    
    res_update    =  model['pig_prod'].update_pig_count(data)
    
    if res_update is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
   
    # remove plain id
    del res_update['pig_prod']['id']
    res_update['pig_prod']['hid'] = pig_prod_hashid


    return res_update
    

@app.post("/production_group/add", tags=["Pig Production"])
async def production_group_add(request: Request):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_FEED_BALANCE_INVALID_USER_HASHID,
                'code': 'ERROR_FEED_BALANCE_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    
    
    
    data = None
    
    try:
        # Parse JSON data from request body
        data = await request.json()
    except:
        data = None
        
    
    
    group_hid       = data.get('group_hid', None)
    list_prod_hid   = data.get('list_prod_hid', [])
    
    
    group_id    = None
    
    if group_hid is not None:
        res = hashids_common.decrypt(group_hid)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_HASHID'
                }
            }
        
        group_id = res[0]
        
        
    list_pig_prod_id = []
    
    for cur_entry in list_prod_hid:
        res = hashids_common.decrypt(cur_entry)
        if len(res) == 0:
            return {
                'result':{
                    'num':  ERROR_PIG_PROD_INVALID_HASHID,
                    'code': 'ERROR_PIG_PROD_INVALID_HASHID'
                }
            }
        
        pig_prod_id = res[0]
        
        list_pig_prod_id.append(pig_prod_id )
        
    
    dt_now          = datetime.now()
    dt_now_s        = dt_now.strftime('%Y-%m-%d')
        
        
    if group_id is None:
        res_group   = None
        
        prod_group_id = 0
    
        # Process the entries
        count = 0
        for cur_entry in list_pig_prod_id:
            if count == 0:
                data = {
                    'user_id':      user_id,
                    'pig_prod_id':  cur_entry,
                    'date_added':   dt_now_s
                }
                
                res_group = model['pig_prod'].create_group(data)
                
                if res_group is None:
                    return {
                        'result':{
                            'num':  ERROR_DATABASE_ERROR,
                            'code': 'ERROR_DATABASE_ERROR'
                        }
                    }
                
                prod_group_id = res_group['pig_prod']['id']
                    
            else:
                data = {
                    'user_id':      user_id,
                    'prod_group_id': prod_group_id,
                    'pig_prod_id':  cur_entry,
                    'date_added':   dt_now_s
                }
                
                res_add = model['pig_prod'].add_to_group(data)
                
                if res_add is None:
                    return {
                        'result':{
                            'num':  ERROR_DATABASE_ERROR,
                            'code': 'ERROR_DATABASE_ERROR'
                        }
                    }
                
                
            
            count += 1 
        
        
        # Replace plain id
        pig_prod_id     = res_group['pig_prod']['id']        
        pig_prod_hashid = hashids_common.encrypt(pig_prod_id)
        
       
        # remove plain id
        del res_group['pig_prod']['id']
        res_group['pig_prod']['hid'] = pig_prod_hashid


        # Remove optional desc coming from database
        remove_database_null_description(res_group)

        return res_group
        
    

    return {
        'result':{
            'num':  0
        }
    }


