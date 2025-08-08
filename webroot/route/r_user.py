# January 4, 2024
# Jack Wong

import os
import sys

from pydantic               import BaseModel
    
sys.path.append('..')
from common_constants       import *
from common_app             import *
from common_fast_api        import *

    
@app.post("/testing/user/hashid/{user_id}")
async def testing_user_hashid(user_id: int):
    """
    Will return hashid for user.id
    """
    
    return hashids_user.encrypt(user_id)
    


