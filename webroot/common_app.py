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


"""
# Default configuration file
#CONFIGURATION_FILE          = path_app + '/project/cyfi.config'


# Read Config file
config_file = open(CONFIGURATION_FILE, 'r')
config_json = json.loads(config_file.read())
config_file.close()
"""



# Create logger
logger      = common_logger.Logger(path_logs = path_logs, log_name = 'web')
s = '\n\nStarting Pig Operations application\n'
logger.append(tag = 'Main', msg = s)

"""
# Models for connecting to booking database

from model.m_lookup             import Lookup
from model.m_address            import Address
from model.m_location_adrs      import LocationAddress
from model.m_contact            import Contact

from model.m_user               import User
from model.m_booking            import Booking

model_names_booking = [
    ('lookup',                  Lookup),
    ('address',                 Address),
    ('location_adrs',           LocationAddress),
    
    ('contact',                 Contact),
    ('user',                    User),
    ('booking',                 Booking)
]


credentials = {
    'db_host':      'localhost',
    'db_user':      'book_web',
    'db_password':  '1@LGTK_BOOK#db$1234.',
    'database':     'booking'
}


model = Model(database_id = 1, logger = logger, credentials = credentials)
model.append_models(model_names_booking)
"""


from model.m_sow_act            import SowActivity

# Models for connecting to database
model_names = [
    ('sow_act',                 SowActivity)
]


DATABASE_NAME_PIG_OPERATIONS = 'po'


"""
The MySQL credentials below is taken from this connection string.

mysql://6vni666euhid4v77r5js:pscale_pw_O3uV46HuFWlEwMtmrhlZ29AqlwtMe5rLQeuAdZJT8vr@ap-southeast.connect.psdb.cloud/eforwardmo-prod?sslaccept=strict
"""

def extract_db_credentials(s):
    """
    Will extract mysql database credentials from connection string.
    
    Parameters
    ----------
    s : str
        connection string
        
    Returns
        dictionary
    """
    
    index = s.find('://')
    if index < 0:
        return None
        
    index_b     = index + 3
    index_e     = s.find(':', index_b)
    db_user     = s[index_b: index_e]
    
    index_b     = index_e + 1
    index_e     = s.find('@', index_b)
    db_password = s[index_b: index_e]
    
    index_b     = index_e + 1
    index_e     = s.find('?', index_b)
    db_host     = s[index_b: index_e]
    
    return {
        'db_host':     db_host,
        'db_user':     db_user,
        'db_password': db_password,
        'database':    DATABASE_NAME_CONTAINER_BOOKING
    }
    

credentials_po = {
    'db_host':      '127.0.0.1',
    'db_user':      'pops_web',
    'db_password':  '1@PO#db$1234.',
    'database':     DATABASE_NAME_PIG_OPERATIONS
}



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

COMMON_HASH_ALPHABET                    = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

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





"""
from route.address_manager          import AddressManager
address_mngr    = AddressManager()
address_mngr.load_level_address()
"""

ENABLE_HASHIDS          = 1
ENABLE_BEARER_TOKEN     = 0


