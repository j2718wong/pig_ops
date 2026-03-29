# March 16, 2024
# Jack Wong

import os
import sys
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



from report_prod_ops        import ReportProdOps
from formatters.f_pdf       import F_PDF



# Initialize once
report_generator    = ReportProdOps()
pdf_formatter       = F_PDF(template_dir=os.path.join(webroot_directory, 'templates_report'))



MIN_DAYS_REPORT     = 8


    
@app.get("/report/pig_farm/summary", tags=["Report"])
async def report_pig_farm_summary(uhid:str, pfhid:str, inc_historical: int =0, 
        inc_cost: int = 0, inc_target_harvest: int= 0, year:int = None):
    """
    Will generate pig_prod operations report.

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
    


