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
    

