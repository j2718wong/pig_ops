# December 5, 2024
# Jack Wong (zhaoshan99@gmail.com)

import os
import sys



# import packages
import json
import hashids
import math

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
from model.m_account_request    import AccountRequest
from model.m_mfa                import Mfa

from model.m_user               import User
from model.m_user_group         import UserGroup
from model.m_user_pig_farm      import UserPigFarm


from model.m_pig_farm           import PigFarm
from model.m_pig_farm_staff     import PigFarmStaff

from model.m_account_selection  import AccountSelection
from model.m_account_pig_ops    import AccountPigOps
from model.m_account_pig_buyer  import AccountPigBuyer

from model.m_common_supplier    import CommonSupplier
from model.m_public_report      import PublicReport

from model.m_pig_race           import PigRace
from model.m_pig_race_line      import PigRaceLine
from model.m_semen_supplier_semen import SemenSupplierSemen

from model.m_feed_type          import FeedType
from model.m_feed_brand         import FeedBrand
from model.m_feed_supplier      import FeedSupplier
from model.m_feed_buy           import FeedBuy
from model.m_feed_balance       import FeedBalance
from model.m_feed_calc          import FeedCalc

from model.m_medvac_brand       import MedVacBrand
from model.m_medvac_type        import MedVacType

from model.m_sow_boar           import SowBoar

from model.m_sow_act            import SowActivity


from model.m_pig_production     import PigProduction
from model.m_pig_prod_notes     import PigProdNotes
from model.m_pig_prod_pig_dead  import PigProdPigDead
from model.m_pig_prod_pig_ops   import PigProdPigOps

from model.m_pig_medvac         import PigMedVac

from route.controller           import Controller

from view.view                  import View


# Models for connecting to database
model_names_pig_ops = [
    ('app_analytics',           AppAnalytics),

    ('account',                 Account),
    ('acc_req',                 AccountRequest),
    ('mfa',                     Mfa),
    
    ('user',                    User),
    ('user_group',              UserGroup),
    ('user_farm',               UserPigFarm),
    
    
    ('pig_farm',                PigFarm),
    ('pig_farm_staff',          PigFarmStaff),
    
    
    ('account_selection',       AccountSelection),
    ('account_pig_ops',         AccountPigOps),
    ('account_pig_buyer',       AccountPigBuyer),
    
    ('supplier',                CommonSupplier),
    ('public_report',           PublicReport),
    
    ('pig_race',                PigRace),
    ('pig_race_line',           PigRaceLine),
    
    ('semen_sup_semen',         SemenSupplierSemen),
    
    ('feed_type',               FeedType),
    ('feed_brand',              FeedBrand),
    ('feed_supplier',           FeedSupplier),
    ('feed_buy',                FeedBuy),
    ('feed_balance',            FeedBalance),
    ('feed_calc',               FeedCalc),
    
    ('medvac_brand',            MedVacBrand),
    ('medvac_type',             MedVacType),
    
    
    ('sow_boar',                SowBoar),
   
    
    ('pig_prod',                PigProduction),
    ('prod_notes',              PigProdNotes),
    ('prod_pig_dead',           PigProdPigDead),
    ('pig_prod_pig_ops',        PigProdPigOps),
    
    ('pig_medvac',              PigMedVac),
    
    ('sow_act',                 SowActivity)
    
 
]



DEV_OFFICE                      = 0
DEV_HOME                        = 1



# Change thee settings for development
USING_PRODUCTION_DB             = 0
USING_DEV_AT                    = DEV_HOME
DB_INFO                         = ''



if USING_PRODUCTION_DB > 0:
    DATABASE_NAME_PIG_OPERATIONS = 'pig_operations'
    db_desc     = 'Jackson Farm Production'

    credentials_po = {
        'db_host':      '127.0.0.1',
        'db_user':      'pops_web',
        'db_password':  '1@PO#db$1234.',
        'database':     DATABASE_NAME_PIG_OPERATIONS
    }

    
    ssh_tunnel_prod = {
        'ssh_host':         '10.10.2.62',
        'ssh_port':         22,
        'ssh_username':     'dev01',
        'ssh_password':     '0@DEV12345.',
        'ssh_pkey':         None,

        'remote_hostname':  '127.0.0.1',
        'remote_port':      3306,
        'local_hostname':   '127.0.0.1',
        'local_port':       3307
    }
    
    if USING_DEV_AT == DEV_HOME:
        ssh_tunnel_prod['ssh_host'] = '192.168.0.166'
    
    
    print('\n\nWill use PRODUCTION database\n\n')
else:
    DATABASE_NAME_PIG_OPERATIONS = 'pig_operations'
    db_desc     = 'Jackson Farm Production'

    credentials_po = {
        'db_host':      '127.0.0.1',
        'db_user':      'pops_web',
        'db_password':  '1@PO#db$1234.',
        'database':     DATABASE_NAME_PIG_OPERATIONS
    }

    
    ssh_tunnel_prod = {
        'ssh_host':         '10.10.2.62',
        'ssh_port':         22,
        'ssh_username':     'dev01',
        'ssh_password':     '0@DEV12345.',
        'ssh_pkey':         None,

        'remote_hostname':  '127.0.0.1',
        'remote_port':      4306,
        'local_hostname':   '127.0.0.1',
        'local_port':       3307
    }
    
    if USING_DEV_AT == DEV_HOME:
        ssh_tunnel_prod['ssh_host'] = '192.168.0.166'
    
    
    print('\n\nWill use DEVELOPMENT database\n\n')
    
DB_INFO = f"Host: {credentials_po['db_host']}; DB_Desc: {db_desc}"





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
            credentials     = credentials_po,
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
        'db_host':      '127.0.0.1',
        'db_user':      'ladrs_web',
        'db_password':  '1@LADRS#db$1234.',
        'database':     DATABASE_NAME_LOC_ADDRESS
    }



else:
    DATABASE_NAME_LOC_ADDRESS = 'loc_address'
    db_desc     = 'JSysDev Location address' 
    
    credentials_la = {
        'db_host':      '127.0.0.1',
        'db_user':      'ladrs_web',
        'db_password':  '1@LADRS#db$1234.',
        'database':     DATABASE_NAME_LOC_ADDRESS
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

ssh_tunnel = ssh_tunnel_la
try:
    database_loc = os.environ['PO_DATABASE_LOC']
    if database_loc == 'LOCAL':
        ssh_tunnel = None
except:
    ssh_tunnel = ssh_tunnel_la


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

HASHID_SALT_COMMON                      = '68FD4C'
HASHID_MIN_LENGTH_COMMON                = 6

hashids_common  = hashids.Hashids(  salt        = HASHID_SALT_COMMON, 
                                    min_length  = HASHID_MIN_LENGTH_COMMON,
                                    alphabet    = COMMON_HASH_ALPHABET)


HASHID_SALT_USER                        = '28A05B'
HASHID_MIN_LENGTH_USER                  = 6

hashids_user    = hashids.Hashids(  salt        = HASHID_SALT_USER, 
                                    min_length  = HASHID_MIN_LENGTH_USER,
                                    alphabet    = COMMON_HASH_ALPHABET)



HASHID_SALT_ACCOUNT                     = '9C069A'
HASHID_MIN_LENGTH_ACCOUNT               = 6

hashids_account = hashids.Hashids(  salt        = HASHID_SALT_ACCOUNT, 
                                    min_length  = HASHID_MIN_LENGTH_ACCOUNT,
                                    alphabet    = COMMON_HASH_ALPHABET)


# Manager to to request address level names from a different server
adrs_level_mngr = AddressManager(logger)


ENABLE_HASHIDS          = 1
ENABLE_BEARER_TOKEN     = 0




controller = Controller(logger, model)
view = View(controller)