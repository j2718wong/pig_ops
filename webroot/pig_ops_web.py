# December 13, 2024
# Jack Wong (zhaoshan99@gmail.com)

import uvicorn

from common_fast_api            import *
from common_app                 import *

from route.r_sow_act            import *

from route.r_user               import *
from route.r_user_group         import *
from route.r_account            import *
from route.r_account_request    import *

from route.r_pig_farm           import *

from route.r_acc_gestating_ops  import *

from route.r_pig_race           import *
from route.r_pig_race_line      import *
from route.r_semen_supplier     import *

from route.r_feed_brand         import *
from route.r_feed_supplier      import *

from route.r_semen_source       import *
from route.r_sow_boar           import *

from route.r_pig_production     import *

from route.r_testing            import *


@app.get("/test")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    
    uvicorn.run("pig_ops_web:app", host='0.0.0.0', port=8080)
        


