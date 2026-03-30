# March 16, 2024
# Jack Wong

import os
import sys
import random
import pprint


from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse, Response

from datetime               import datetime, timedelta 

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *

from fastapi.responses      import PlainTextResponse


import data_model           as dm


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
webroot_directory           = os.path.dirname(os.path.dirname(module_file_path))


report_dir = os.path.join(webroot_directory, 'report')
if report_dir not in sys.path:
    sys.path.insert(0, report_dir)


DEFAULT_REPORT_TRANSLATION = {
    "generated_on":         "Petsa Pagbuhat",
        
    "leg_done_on_time":     "Done on time",
    "leg_done_late":        "Done late",
    "leg_done_very_late":   "Done very late",
    "leg_overdue":          "Overdue",
    "leg_sow_operation":    "Sow Operation",
    "leg_piglet_operation": "Piglet Operation",
    
    "gestating_sows_title": "Gestating Sows (Pregnant)",
    "gestating_sows":       "Gestating Sows",
    "pid_sow":              "PID / Sow",
    "date_mating":          "Date Mating",
    "boar_semen":           "Boar/Semen",
    "expected_birth":       "Expected Birth",
    
    "lactating_sows_title": "Lactating Sows",    
    "lactating_sows":       "Lactating Sows",
    "sow_operations":       "Sow Operations",
    "piglet_operations":    "Piglet Operations",
    "date_of_birth":        "Date of Birth",
    "expected_wean":        "Expected Wean",
    "pigs":                 "Pigs",
    
    "feed_change_record":   "Feed Change Record",
    
    "lactating_piglets":    "Lactating Piglets",
    "fattening_pigs":       "Fattening",
    "total_pigs":           "Total Pigs",
    "total_piglets":        "Total Piglets",
    
    "date_harvest":         "Date Harvest",
    "target":               "Target",
        
    "total_entries":        "Total Entries",
    "batches":              "batches",
    
    
    "prod_feed_consumption": "Prod Feed Consumption",
    
    "pid":                  "PID",
    "prod_status":          "Prod Status",
    "feed_bal_date":        "Feed Bal Date",  
        
    "balance_total":        "Total Balance"
}


DEFAULT_NO_ENTRIES_TABLE = ['No records found', 'No Entries', 'No Data', 'Nothing in here']




from report_prod_ops        import ReportProdOps
from formatters.f_pdf       import F_PDF



# Initialize once
report_generator    = ReportProdOps()
pdf_formatter       = F_PDF(template_dir=os.path.join(webroot_directory, 'templates_report'))



MIN_DAYS_REPORT     = 8


    
@app.get("/report/pig_farm/summary", tags=["Report"])
async def report_pig_farm_summary(uhid:str, pfhid:str, language = None,
        inc_historical: int =0, inc_cost: int = 0, inc_target_harvest: int= 0, 
        year:int = None):
    """
    Will generate pig_farm_summary report.

    Parameters
    ==========
    
    uhid : str
        user hash id
        
    pfhid : str
        pig farm hash id
       
    inc_historical : int
        if > 0, pig production with status lactating, growing, harvested, 
        close will be returned
    
    inc_cost : int
        if > 0, will include feeds cost
        
    inc_target_harvest : int
        if > 0, will compute target harvest date
        
    """
    

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result': {
                'num': ERROR_PIG_PROD_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result': {
                'num': ERROR_PIG_PROD_OPS_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_PIG_PROD_OPS_INVALID_PIG_FARM_HASHID',
                'desc': ''
            }
        }
    
    pig_farm_id = res[0]
    
    
    # Get data
    data = report_generator.get_data(pig_farm_id, inc_historical=inc_historical)


    # Set report language
    translations = DEFAULT_REPORT_TRANSLATION
    
    if language is not None:
        lang_code = controller.get_language_key(language)
        
        if lang_code:
            all_translations = controller.translations[lang_code]
            
            if all_translations:
                translations = all_translations['reports']
                
                # Special case for No entries
                translated_no_entries = all_translations['common']['labels']['no_entries']
                
                en_no_entries       = random.choice(DEFAULT_NO_ENTRIES_TABLE)
                local_no_entries    = random.choice(translated_no_entries)
                
                translations['no_entries'] = en_no_entries + '; ' + local_no_entries
                

    # Generate PDF
    pdf_bytes = pdf_formatter.generate_pig_farm_summary_report(data, translations)
    
    
    # Generate filename
    farm_name           = data['pig_farm_info']['pig_farm']['name'].replace(' ', '_')
    filename            = f"gestating_report_{farm_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    
    # Record analytics
    data_analytics = {
        'user_id':          user_id,
        'app_function_id':  APP_ANALYTICS_ID_REPORT_GESTATING_PDF  
    }
    model['app_analytics'].add(data_analytics)
    
    
    # Return PDF response
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "application/pdf"
        }
    )
    


@app.post("/report/pig_farm/summary/add", tags=["Report"])
async def report_pig_farm_summary_add(request: Request, data: dm.DataReport):
    """
    Will generate pig_farm_summary report.

    """
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
                'num':  ERROR_USER_INVALID_USER_HASHID,
                'code': 'ERROR_USER_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    
    
    
    # Checks if user is valid, if account is valid, if account has due bill
    res_check = check_if_valid_user_account(user_id)

    if res_check['inv_result'] != None:
        return res_check['inv_result']
        
    new_bill_hid = res_check['new_bill_hid']
    

    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result': {
                'num': ERROR_PIG_PROD_OPS_INVALID_USER_HASHID,
                'code': 'ERROR_PIG_PROD_OPS_INVALID_USER_HASHID',
                'desc': ''
            }
        }
    
    user_id = res[0]
    
    
    pig_farm_hid        = data.pig_farm_hid
    
    res = hashids_common.decrypt(pig_farm_hid)
    if len(res) == 0:
        result =  {
            'result':{
                'num':  ERROR_PF_FEED_BUY_INVALID_PIG_FARM_HASHID,
                'code': 'ERROR_PF_FEED_BUY_INVALID_PIG_FARM_HASHID'
            }
        }
        
        if new_bill_hid is not None:
            result['result']['new_bill_hid'] = new_bill_hid
        
        return result
        
    pig_farm_id = res[0]
    
    
    
    # Get data
    data.user_id        = user_id
    data.pig_farm_id    = pig_farm_id
    
    
    data_report = report_generator.get_data(pig_farm_id)
    
    
    # Get Report language
    report_language = data.language
    
    lang_code = controller.get_language_key(report_language)
    

    
    # Generate PDF
    pdf_bytes           = pdf_formatter.generate_pig_farm_summary_report(data)
    
    
    # Generate filename
    farm_name           = data['pig_farm_info']['pig_farm']['name'].replace(' ', '_')
    filename            = f"gestating_report_{farm_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    
    # Record analytics
    data_analytics = {
        'user_id':          user_id,
        'app_function_id':  APP_ANALYTICS_ID_REPORT_GESTATING_PDF  
    }
    model['app_analytics'].add(data_analytics)
    
    
    # Return PDF response
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "application/pdf"
        }
    )








@app.get("/report/list", tags=["Report"])
async def report_list(request: Request, pfhid: str = None, rtid: int = 1,
        date_min = None):
    """
    Will get pig ram report list.
    
    Parameters
    ----------
    pfhid : str
        pig farm hid;
        
    rtid : int
        report type id
    
    date_min : str
        date minimum; if not given this is today - MIN_DAYS_REPORT
    
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    pig_farm_id = 0

    
    res = hashids_common.decrypt(pfhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_PIG_FARM_INVALID_HASHID,
                'code': 'ERROR_PIG_FARM_INVALID_HASHID'
            }
        }
    
    pig_farm_id = res[0]
    
    
    if date_min is None:
        dt_now      = datetime.now()
        dt_min      = dt_now - timedelta(days = MIN_DAYS_REPORT)
        dt_min_s    = datetime.strftime(dt_min, '%Y-%m-%d')
    
    else:
        dt_min      = datetime.strptime(data.date_mate, '%Y-%m-%d')
        dt_min_s    = datetime.strftime(dt_min, '%Y-%m-%d')
    
    
    
    res = model['report'].get_list(pig_farm_id, rtid, date_min = dt_min_s)
    
    if res is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    

    for cur_entry in res:
        cur_id  = cur_entry['report']['id']
        cur_hid = hashids_common.encrypt(cur_id)
    
        del cur_entry['report']['id']
        cur_entry['report']['hid']   = cur_hid
        
        
    return {
        'result':{
            'num':  0
        },
        
        'data': res
    }
    


