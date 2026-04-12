# December 13, 2024
# Jack Wong (zhaoshan99@gmail.com)
import os
import uvicorn

from common_fast_api            import *
from common_app                 import *

from route.r_a0_etc             import *

from route.r_sow_act            import *
from route.r_prod_ops           import *

from route.r_user               import *
from route.r_user_request       import *
from route.r_user_group         import *
from route.r_account            import *
from route.r_account_access_code import *


from route.r_business           import *

from route.r_customer           import *

from route.r_address_level      import *

from route.r_a0_public_lookup   import *


from route.r_pig_farm           import *
from route.r_pig_farm_staff     import *
from route.r_pig_farm_feed_buy  import *
from route.r_pig_farm_feed_buy_item  import *

from route.r_account_selection  import *
from route.r_account_pig_ops    import *
from route.r_account_medvac     import *
from route.r_account_pig_buyer  import *

from route.r_public_report      import *
from route.r_common_supplier    import *

from route.r_pig_race           import *
from route.r_pig_race_line      import *
from route.r_semen_sup_semen    import *


from route.r_feed_brand         import *
from route.r_feed_supplier      import *
from route.r_feed_buy           import *
from route.r_feed_balance       import *
from route.r_feed_calc          import *

from route.r_sow_boar           import *
from route.r_sow_boar_mate      import *

from route.r_pig_production     import *
from route.r_pig_production_get import *
from route.r_pig_prod_notes     import *
from route.r_pig_prod_pig_dead  import *
from route.r_pig_prod_pig_ops   import *

from route.r_medvac_brand       import * 
from route.r_medvac_type        import *
from route.r_pig_medvac         import *

from route.r_production_harvest import *


from route.r_report             import *

from route.r_testing            import *


from route.r_a0_root            import *


"""
@app.get("/test")
async def test():
    return {"message": "Hello World"}
"""

# Print all routes
"""
@app.on_event("startup")
def list_routes():
    print("\n=== All Registered Routes ===\n")
    for route in app.routes:
        methods = getattr(route, "methods", None)
        name = getattr(route, "name", None)
        path = getattr(route, "path", None)
        
        if methods:
            methods_str = ", ".join([m for m in methods if m])
            print(f"{methods_str:10} {path} {name or ''}")
    print("=" * 40)
"""


import ssl


if __name__ == '__main__':
    """
    2026-03-16 Orig without certificate
    # Get port from environment variable, default to 8080 if not set
    port = int(os.getenv('PORT_WEB', '8080'))
    
    uvicorn.run("pig_ops_web:app", host='0.0.0.0', port=port)
    """
    
    port = int(os.getenv('PORT_WEB', '8080'))
    use_https = os.getenv('USE_HTTPS', 'false').lower() == 'true'
    
    if use_https:
        # SSL Context for HTTPS
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(
            'localhost+4.pem',        # Your certificate
            keyfile='localhost+4-key.pem'  # Your private key
        )
        
        uvicorn.run(
            "pig_ops_web:app",
            host='0.0.0.0',
            port=8443,  # HTTPS port
            ssl=ssl_context
        )
    else:
        # Regular HTTP mode
        uvicorn.run(
            "pig_ops_web:app",
            host='0.0.0.0',
            port=port
        )
    
    
    


