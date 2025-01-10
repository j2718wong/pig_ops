# December 13, 2024
# Jack Wong (zhaoshan99@gmail.com)

import uvicorn

from common_fast_api        import *
from common_app             import *

from route.r_sow_act           import *



from route.r_testing        import *
    

@app.get("/test")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run("pig_ops_web:app", host='0.0.0.0', port=5000, reload=True)
        


