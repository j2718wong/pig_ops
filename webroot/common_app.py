# December 5, 2024
# Jack Wong (zhaoshan99@gmail.com)

import os
import sys



# import packages
import json
import hashids
import math


from pathlib    import Path
from dotenv     import load_dotenv


# import modules from path_common
import common_logger

from common_constants       import *

from model.database_conn    import *

from address_manager        import AddressManager


cur_path        = os.getcwd()
path_logs       = os.path.join(cur_path, 'data', 'logs')



# Create logger
logger      = common_logger.Logger(path_logs = path_logs, log_name = 'web')
s = '\n\nStarting Pig Operations application\n'
logger.append(tag = 'Main', msg = s)


from model.m_app_analytics      import AppAnalytics

from model.m_account            import Account
from model.m_account_access_code import AccountAccessCode


from model.m_a0_public_lookup   import PublicLookup

from model.m_customer_feedback  import CustomerFeedback


from model.m_user               import User
from model.m_user_request       import UserRequest
from model.m_user_group         import UserGroup
from model.m_user_pig_farm      import UserPigFarm


from model.m_pig_farm           import PigFarm
from model.m_pig_farm_staff     import PigFarmStaff
from model.m_pig_farm_feed_buy  import PigFarmFeedBuy
from model.m_pig_farm_feed_buy_item  import PigFarmFeedBuyItem


from model.m_account_selection  import AccountSelection
from model.m_account_pig_ops    import AccountPigOps
from model.m_account_medvac     import AccountMedVac
from model.m_account_pig_buyer  import AccountPigBuyer

from model.m_common_supplier    import CommonSupplier
from model.m_public_report      import PublicReport

from model.m_pig_race           import PigRace
from model.m_pig_race_line      import PigRaceLine
from model.m_semen_supplier_semen import SemenSupplierSemen


from model.m_feed_brand         import FeedBrand
from model.m_feed_supplier      import FeedSupplier
from model.m_feed_buy           import FeedBuy
from model.m_feed_balance       import FeedBalance
from model.m_feed_calc          import FeedCalc

from model.m_medvac_brand       import MedVacBrand
from model.m_medvac_type        import MedVacType

from model.m_sow_boar           import SowBoar
from model.m_sow_boar_mate      import SowBoarMate

from model.m_sow_act            import SowActivity


from model.m_pig_production     import PigProduction
from model.m_pig_prod_notes     import PigProdNotes
from model.m_pig_prod_pig_dead  import PigProdPigDead
from model.m_pig_prod_pig_ops   import PigProdPigOps
from model.m_pig_prod_feed      import PigProdFeed

from model.m_production_harvest import ProductionHarvest

from model.m_pig_medvac         import PigMedVac

from model.m_report             import Report

from route.controller           import Controller

from view.view                  import View


# Models for connecting to database
model_names_pig_ops = [
    ('app_analytics',           AppAnalytics),

    ('account',                 Account),
    ('access_code',             AccountAccessCode),
    
    ('cust_feedback',           CustomerFeedback), 
    
    ('user',                    User),
    ('user_req',                UserRequest),
    ('user_group',              UserGroup),
    ('user_farm',               UserPigFarm),
    
    ('public_lookup',           PublicLookup),
    
    
    ('pig_farm',                PigFarm),
    ('pig_farm_staff',          PigFarmStaff),
    ('pf_feed_buy',             PigFarmFeedBuy),
    ('pf_feed_buy_item',        PigFarmFeedBuyItem),
    
    
    ('account_selection',       AccountSelection),
    ('account_pig_ops',         AccountPigOps),
    ('account_medvac',          AccountMedVac),
    
    ('account_pig_buyer',       AccountPigBuyer),
    
    ('supplier',                CommonSupplier),
    ('public_report',           PublicReport),
    
    ('pig_race',                PigRace),
    ('pig_race_line',           PigRaceLine),
    
    ('semen_sup_semen',         SemenSupplierSemen),
    
    
    ('feed_brand',              FeedBrand),
    ('feed_supplier',           FeedSupplier),
    ('feed_buy',                FeedBuy),
    ('feed_balance',            FeedBalance),
    ('feed_calc',               FeedCalc),
    
    ('medvac_brand',            MedVacBrand),
    ('medvac_type',             MedVacType),
    
    
    ('sow_boar',                SowBoar),
    ('sow_boar_mate',           SowBoarMate),
    
   
    
    ('pig_prod',                PigProduction),
    ('prod_notes',              PigProdNotes),
    ('prod_pig_dead',           PigProdPigDead),
    ('pig_prod_pig_ops',        PigProdPigOps),
    ('pig_prod_feed',           PigProdFeed),
    
    ('prod_harvest',            ProductionHarvest),
    
    ('pig_medvac',              PigMedVac),
    
    ('report',                  Report),
    
    ('sow_act',                 SowActivity)
    
 
]




# Change this settings for development
USING_PRODUCTION_DB             = 0

DB_INFO                         = ''



# Get APP_ENVI
app_envi = os.getenv('APP_ENVI', 'development')
if app_envi == 'production':
    USING_PRODUCTION_DB = 1
else:
    USING_PRODUCTION_DB = 0

print('\n\nAPP_ENVI = %s' %app_envi)





if USING_PRODUCTION_DB > 0:
    db_desc     = 'Production'

    credentials_pig_ops = {
        'db_host':          os.getenv('PIG_OPS_PROD_DB_HOST', '127.0.0.1'),
        'db_user':          os.getenv('PIG_OPS_PROD_DB_USER'),
        'db_password':      os.getenv('PIG_OPS_PROD_DB_PASSWORD'),
        'database':         os.getenv('PIG_OPS_PROD_DB_NAME', 'pig_operations')
    }

    

    
    ssh_tunnel_prod = {
        'ssh_host':         os.getenv('PIG_OPS_SSH_HOST'),
        'ssh_port':         os.getenv('PIG_OPS_SSH_PORT'),
        'ssh_username':     os.getenv('PIG_OPS_SSH_USERNAME'),
        'ssh_password':     os.getenv('PIG_OPS_SSH_PASSWORD'),
        'ssh_pkey':         os.getenv('PIG_OPS_SSH_PKEY_PATH'),

        'remote_hostname':  '127.0.0.1',
        'remote_port':      4306,
        'local_hostname':   '127.0.0.1',
        'local_port':       3307
    }
    
    
    # 2026-02-04 Direct at server machine
    ssh_tunnel_prod = None
    
    print('\n\nWill use PRODUCTION database\n\n')

else:
    db_desc     = 'Development'

    credentials_pig_ops = {
        'db_host':          os.getenv('PIG_OPS_DEV_DB_HOST', '127.0.0.1'),
        'db_user':          os.getenv('PIG_OPS_DEV_DB_USER'),
        'db_password':      os.getenv('PIG_OPS_DEV_DB_PASSWORD'),
        'database':         os.getenv('PIG_OPS_DEV_DB_NAME', 'pig_ops_dev')
    }

    
    ssh_tunnel_prod = {
        'ssh_host':         os.getenv('PIG_OPS_SSH_HOST'),
        'ssh_port':         os.getenv('PIG_OPS_SSH_PORT'),
        'ssh_username':     os.getenv('PIG_OPS_SSH_USERNAME'),
        'ssh_password':     os.getenv('PIG_OPS_SSH_PASSWORD'),
        'ssh_pkey':         os.getenv('PIG_OPS_SSH_PKEY_PATH'),

        'remote_hostname':  '127.0.0.1',
        'remote_port':      4306,
        'local_hostname':   '127.0.0.1',
        'local_port':       3307
    }
    

    
    
    # 2026-02-04; something is wrong with paramiko when using SSH Tunnel
    ssh_tunnel_prod = None
    
    print('\n\nWill use DEVELOPMENT database\n\n')
    

DB_INFO = f"Host: {credentials_pig_ops['db_host']}; DB_Desc: {db_desc}"





ssl_po = {'ca': None}


# Read PO_DATABASE_LOC environment variable if there is any.
# This environment variable is used to control what database to access.

ssh_tunnel = ssh_tunnel_prod
try:
    database_loc = os.environ['PO_DATABASE_LOC']
    if database_loc == 'LOCAL':
        ssh_tunnel = None
except:
    ssh_tunnel = ssh_tunnel_prod


model = Model(
            database_id     = 1, 
            logger          = logger, 
            credentials     = credentials_pig_ops,
            ssl             = None,
            tunnel_settings = ssh_tunnel_prod)

            
model.append_models(model_names_pig_ops)



from model.m_address_level      import AddressLevel
model_names_la = [
    ('address_level',           AddressLevel)
    
]



if USING_PRODUCTION_DB > 0:
    DATABASE_NAME_LOC_ADDRESS = 'loc_address'
    db_desc     = 'JSysDev Location address'

    credentials_la = {
        'db_host':          os.getenv('LOC_ADDRESS_DB_HOST', '127.0.0.1'),
        'db_user':          os.getenv('LOC_ADDRESS_DB_USER'),
        'db_password':      os.getenv('LOC_ADDRESS_DB_PASSWORD'), 
        'database':         os.getenv('LOC_ADDRESS_DB_NAME', DATABASE_NAME_LOC_ADDRESS) 
    }



else:
    # For now same
    
    DATABASE_NAME_LOC_ADDRESS = 'loc_address'
    db_desc     = 'JSysDev Location address' 
    
    credentials_la = {
        'db_host':          os.getenv('LOC_ADDRESS_DB_HOST', '127.0.0.1'),
        'db_user':          os.getenv('LOC_ADDRESS_DB_USER'),
        'db_password':      os.getenv('LOC_ADDRESS_DB_PASSWORD'), 
        'database':         os.getenv('LOC_ADDRESS_DB_NAME', DATABASE_NAME_LOC_ADDRESS) 
    }




ssh_tunnel_la = {
    'ssh_host':         '192.168.0.166',
    'ssh_port':         22,
    'ssh_username':     'dev01',
    'ssh_password':     '0@DEV12345.',
    'ssh_pkey':         None,

    'remote_hostname':  '127.0.0.1',
    'remote_port':      3306,
    'local_hostname':   '127.0.0.1',
    'local_port':       3308
}


ssl_la = {'ca': None}


# Read PO_DATABASE_LOC environment variable if there is any.
# This environment variable is used to control what database to access.

ssh_tunnel_la = None


model_la = Model(
            database_id     = 2, 
            logger          = logger, 
            credentials     = credentials_la,
            ssl             = None,
            tunnel_settings = ssh_tunnel_la)

            
model_la.append_models(model_names_la)




# Create Hashids
# Letter O is purposely removed so that users will not confused with 0.
COMMON_HASH_ALPHABET                    = 'ABCDEFGHIJKLMNPQRSTUVWXYZ1234567890'

HASHID_SALT_COMMON                      = '68FD4C30'
HASHID_MIN_LENGTH_COMMON                = 8

hashids_common  = hashids.Hashids(  salt        = HASHID_SALT_COMMON, 
                                    min_length  = HASHID_MIN_LENGTH_COMMON,
                                    alphabet    = COMMON_HASH_ALPHABET)


HASHID_SALT_USER                        = '28A05B4A'
HASHID_MIN_LENGTH_USER                  = 8

hashids_user    = hashids.Hashids(  salt        = HASHID_SALT_USER, 
                                    min_length  = HASHID_MIN_LENGTH_USER,
                                    alphabet    = COMMON_HASH_ALPHABET)



HASHID_SALT_ACCOUNT                     = '9C069AF4'
HASHID_MIN_LENGTH_ACCOUNT               = 8

hashids_account = hashids.Hashids(  salt        = HASHID_SALT_ACCOUNT, 
                                    min_length  = HASHID_MIN_LENGTH_ACCOUNT,
                                    alphabet    = COMMON_HASH_ALPHABET)



HASHID_SALT_ACCOUNT_ACCESS_CODE         = '18FB40903'
HASHID_MIN_LENGTH_ACCOUNT               = 8

hashids_access_code = hashids.Hashids(  salt    = HASHID_SALT_ACCOUNT_ACCESS_CODE, 
                                    min_length  = HASHID_MIN_LENGTH_ACCOUNT,
                                    alphabet    = COMMON_HASH_ALPHABET)





# Manager to to request address level names from a different server
adrs_level_mngr = AddressManager(logger)









def get_is_prod_environment():
    """
    This may change in the future; currently this is temporary
    
    Returns 1 if production environment;
    Returns 0 if development environment;
    """
    
    if USING_PRODUCTION_DB > 0:
        return 1
    
    return 0
    

controller = Controller(logger, model)

if get_is_prod_environment() > 0:
    controller.is_prod_envi = True



# Get USE_MINIFIED_JS
temp = os.getenv('USE_MINIFIED_JS', '1')
USE_MINIFIED_JS = 1 
try:
    USE_MINIFIED_JS = int(temp)
except:
    USE_MINIFIED_JS = 1


controller.use_minified_js = USE_MINIFIED_JS


view = View(controller)




def ensure_version_file():
    """Create a default version file if none exists"""
    default_path = os.path.expanduser("~/projects/jsys/version.txt")
    os.makedirs(os.path.dirname(default_path), exist_ok=True)
    
    if not os.path.exists(default_path):
        with open(default_path, 'w') as f:
            f.write("1.0.0.0")
        print(f"Created default version file at {default_path}")

# Create version file if needed
ensure_version_file()




import os
from pathlib import Path

def get_app_version():
    """
    Read and return the current app version from version.txt
    Works in both production and development environments.
    Returns a dict with version info.
    """
    # Try multiple possible locations
    possible_paths = [
        "/root/projects/jsys/version.txt",           # Production
        os.path.expanduser("~/projects/jsys/version.txt"),  # Local dev (Raspberry Pi)
        os.path.join(os.path.dirname(__file__), "../../version.txt"),  # Relative to this file
    ]
    
    version_str = None
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    version_str = f.read().strip()
                    break
        except:
            continue
    
    # If no version file found, use default
    if not version_str:
        version_str = "1.0.0.0"
    
    return version_str
    
    

controller.APP_VERSION = get_app_version()

print('\n\nSuperPig APP_VERSION = %s\n\n' % controller.APP_VERSION)


