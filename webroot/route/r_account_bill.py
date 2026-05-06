# March 19, 2025
# Jack Wong

import os
import sys
import pprint
import shutil
import base64
import mimetypes


from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse, FileResponse

from fastapi                import File, UploadFile, Form

from datetime               import datetime, timedelta
from pathlib                import Path


    
from common_constants       import *
from common_app             import *
from common_fast_api        import *


import data_model           as dm


# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)
webroot_directory           = os.path.dirname(module_directory)

if module_directory not in sys.path:
   sys.path.append(module_directory)


from r_a0_security_checks   import check_if_valid_user_account
from r_utils                import remove_database_null_description



# Configure upload directory base
WEBROOT_DIR         = Path(webroot_directory)
UPLOAD_BASE_DIR     = WEBROOT_DIR / "data" / "account"


    
@app.post("/account_bill/payment_proof/submit", tags=["Account"])
async def account_bill_payment_proof_submit(request: Request,
        account_bill_hid: str = Form(...),
        screenshot: UploadFile = File(...),
    ):
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    
    
    
    res = hashids_user.decrypt(uhid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_BILL_INVALID_USER_HASHID,
                'code': 'ERROR_ACCOUNT_BILL_INVALID_USER_HASHID'
            }
        }
    
    user_id = res[0]
    

    
    res = hashids_common.decrypt(account_bill_hid)
    if len(res) == 0:
        return {
            'result':{
                'num':  ERROR_ACCOUNT_BILL_INVALID_HASHID,
                'code': 'ERROR_ACCOUNT_BILL_INVALID_HASHID'
            }
        }
    
    account_bill_id = res[0]
    

    
    # Get account_info
    user_account = model['user'].get_user_account_info(user_id)
    
    if user_account is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }

    
    # Get account_id
    account_id = user_account['account']['id']
    
    
    """
    The file should be saved in ../webroot/data/account/2026/payment_upload/0002/
    
    where:
        2026 - current year
        0002 - account_id, zero padded; minimum 4 chars


    the filename should be renamed to:
        20260505_204558.<original image file extension>
        
        20260505_204558 - current timestamp

    
    
    root@prod-pig-ops:~/projects/jsys/pig_ops/webroot/data# ls -lt
    total 12
    drwxr-xr-x  2 root root 4096 May  5 02:10 account

    
    the file_path should start at account/...
    """
    
    # Build directory path: ../webroot/data/account/{year}/payment_upload/{account_id_padded}/
    current_year = datetime.now().strftime('%Y')
    account_id_padded = str(account_id).zfill(4)  # Zero pad to 4 digits (e.g., 2 -> 0002)
    
    upload_dir = UPLOAD_BASE_DIR / current_year / "payment_upload" / account_id_padded
    
    
    # Create directory if it doesn't exist
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    
    # Generate filename: {timestamp}.{extension}
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_extension = Path(screenshot.filename).suffix.lower()
    
    # Ensure extension is valid
    if file_extension not in ['.jpg', '.jpeg', '.png']:
        file_extension = '.jpg'  # Default fallback
    
    filename = f"{timestamp}{file_extension}"
    file_path = upload_dir / filename

    
    # Save the file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(screenshot.file, buffer)
            
    except Exception as e:
        return {
            'result':{
                'num':  ERROR_FILE_SAVE_FAILED,
                'code': 'ERROR_FILE_SAVE_FAILED',
                'desc': str(e)
            }
        }
    
    # Build relative file path for database (starts with account/...)
    relative_file_path = f"account/{current_year}/payment_upload/{account_id_padded}/{filename}"
    
    file_path = relative_file_path
    
    
    
    
    data = {
        'user_id':          user_id,
        'account_bill_id':  account_bill_id,
        'file_path':        file_path
    }
    
    pprint.pprint('data to save')
    pprint.pprint(data)
    
    res_add = model['account_bill'].add_upload_receipt(data)
    
    if res_add is None:
        return {
            'result':{
                'num':  ERROR_DATABASE_ERROR,
                'code': 'ERROR_DATABASE_ERROR'
            }
        }
    
    
    # remove plain id
    cur_id    = res_add['upload_receipt']['id']
    cur_hid   = hashids_common.encrypt(cur_id)
    
    del res_add['upload_receipt']['id']
    res_add['upload_receipt']['hid'] = cur_hid

    

    # Remove optional desc coming from database
    remove_database_null_description(res_add)


    return res_add
    

    
@app.get("/account_bill/receipt/{year}/{upload_type}/{account_id}/{filename}")
async def get_receipt_image(
    request: Request,
    year: str,
    upload_type: str,
    account_id: str,
    filename: str
):
    """
    Serve uploaded receipt images.
    URL pattern: /account_bill/receipt/2026/payment_upload/0001/20260505_122949.png
    """
    
    
    """
    result = get_uhid_or_redirect(request)
    
    # If result is RedirectResponse, return it immediately
    if isinstance(result, RedirectResponse):
        return result
    
    
    uhid = result
    """
    
    
    
    # Get the absolute path to webroot
    # This file is in: /path/to/pig_ops/webroot/route/r_account_bill.py
    current_file = Path(__file__).resolve()  # /path/to/pig_ops/webroot/route/r_account_bill.py
    webroot_dir = current_file.parent.parent  # /path/to/pig_ops/webroot/
    
    # Build the absolute file path
    file_path = webroot_dir / "data" / "account" / year / upload_type / account_id / filename
    
    
    # Security: Ensure the path is within the allowed directory
    allowed_dir = webroot_dir / "data" / "account"
    try:
        file_path.resolve().relative_to(allowed_dir.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid file path")
    
    # Check if file exists
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Image not found: {file_path}")
    
    
    # Determine content type
    content_type, _ = mimetypes.guess_type(str(file_path))
    if not content_type:
        content_type = "image/png"
    
    return FileResponse(
        path=file_path,
        media_type=content_type,
        headers={"Cache-Control": "public, max-age=86400"}  # Cache for 1 day
    )


