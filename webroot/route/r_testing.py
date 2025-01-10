# January 4, 2024
# Jack Wong

import os
import sys

from pydantic               import BaseModel
    
sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *

    
@app.get("/testing/user/hashid/{user_id}")
async def testing_user_hashid(user_id: int):
    """
    Will return hashid for user.id
    """
    
    return hashids_user.encrypt(user_id)
    

@app.get("/testing/booking/hashid/{booking_id}")
async def testing_booking_hashid(booking_id: int):
    """
    Will return hashid for booking.id
    """
    
    return hashids_booking.encrypt(booking_id)
    
    
@app.get("/testing/common/hashid/{id}")
async def testing_common_hashid(id: int):
    """
    Will return hashid for an id
    """
    
    return hashids_common.encrypt(id)

