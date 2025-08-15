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




cur_path        = os.getcwd()
path_logs       = os.path.join(cur_path, 'data', 'logs')



# Create logger
logger      = common_logger.Logger(path_logs = path_logs, log_name = 'web')
s = '\n\nStarting Pig Operations application\n'
logger.append(tag = 'Main', msg = s)


from model.m_account            import Account
from model.m_account_request    import AccountRequest
from model.m_mfa                import Mfa

from model.m_pig_farm           import PigFarm
from model.m_sow                import Sow
from model.m_sow_act            import SowActivity
from model.m_user               import User


# Models for connecting to database
model_names = [
    ('account',                 Account),
    ('acc_req',                 AccountRequest),
    ('mfa',                     Mfa),
    
    ('pig_farm',                PigFarm),
    ('sow',                     Sow),
    
    ('sow_act',                 SowActivity),
    ('user',                    User)
    
    
]


USING_PRODUCTION_DB             = 0
DB_INFO                         = ''

if USING_PRODUCTION_DB > 0:
    DATABASE_NAME_PIG_OPERATIONS = 'pig_operations'
    db_desc     = 'Jackson Farm Production'

else:
    DATABASE_NAME_PIG_OPERATIONS = 'pig_ops_dev'
    db_desc     = 'Jackson PigOps Development' 

credentials_po = {
    'db_host':      '127.0.0.1',
    'db_user':      'pops_web',
    'db_password':  '1@PO#db$1234.',
    'database':     DATABASE_NAME_PIG_OPERATIONS
}

DB_INFO = f"Host: {credentials_po['db_host']}; DB_Desc: {db_desc}"


ssh_tunnel_aws = {
    'ssh_host':         'ec2-13-250-35-87.ap-southeast-1.compute.amazonaws.com',
    'ssh_port':         22,
    'ssh_username':     'ubuntu',
    'ssh_password':     None,
    'ssh_pkey':         'sow_prod_key.pem',

    'remote_hostname':  '127.0.0.1',
    'remote_port':      3306,
    'local_hostname':   '127.0.0.1',
    'local_port':       3307
}


ssl_po = {'ca': None}


# Read PO_DATABASE_LOC environment variable if there is any.
# This environment variable is used to control what database to access.

ssh_tunnel = ssh_tunnel_aws
try:
    database_loc = os.environ['PO_DATABASE_LOC']
    if database_loc == 'LOCAL':
        ssh_tunnel = None
except:
    ssh_tunnel = ssh_tunnel_aws


model = Model(
            database_id     = 1, 
            logger          = logger, 
            credentials     = credentials_po,
            ssl             = ssl_po,
            tunnel_settings = ssh_tunnel)

            
model.append_models(model_names)


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



ENABLE_HASHIDS          = 1
ENABLE_BEARER_TOKEN     = 0


