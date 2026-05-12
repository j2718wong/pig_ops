# May 12, 2026
# Jack Wong

import os
import sys
import pprint


from fastapi                import Request, HTTPException, status, Depends
from fastapi.responses      import HTMLResponse, RedirectResponse, PlainTextResponse, Response


from datetime               import datetime, timedelta, date

    
from common_constants       import *
from common_app             import *
from common_fast_api        import *



@app.get("/admin/receipts", response_class = HTMLResponse, dependencies=[Depends(public_limit)])
async def term(response: Response):
    
    page = controller.view['receipts'].render()
    
    return page

