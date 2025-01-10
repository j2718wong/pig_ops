# March 20, 2020
# Jack Wong (zhaoshan99@gmail.com)

import os
import sys

import sshtunnel
import MySQLdb
import socket

"""
To install MySQLdb:
pip install mysqlclient

Debate on which library to use
https://stackoverflow.com/questions/43102442/whats-the-difference-between-mysqldb-mysqlclient-and-mysql-connector-python
"""

# These logging constants are taken from common_constants and should be 
# the same as the common_logger constants. 
LOG_DEBUG               = 0
LOG_WARNING             = 1
LOG_ERROR               = 2
LOG_FATAL               = 3


MAX_NUM_LOOK_AVAILABLE_PORT = 20


class Model:
    """
    This is a model to connect to MySQL database 
    """
    def __init__(self, database_id = 0, logger = None, credentials = None,
            ssl = None, tunnel_settings = None):
        """
        Parameters
        ----------
        
        database_id : integer
            unique identifier of the database to connect.
        
        logger : commmon_logger.Logger object
        
        credentials : dictionary 
            This is a structure similar to this :: 
              
                {
                    'db_host':      'localhost',
                    'db_user':      'DbCredentialsWeb',
                    'db_password':  '****',
                    'database':     'DATABASE'
                }
        
        ssl: dictionary, optional
            This is a dictionary like this ::
            
                {
                    'ca': '/path/to/ca/ca',
                    'key': '/path/to/ca/key',
                    'cert': '/path/to/ca/cert'
                }
            
        
        tunnel_settings : dictionary, optional 
            if the application needs to SSH to host, this must be provided.
        
            This must be similar to this structure ::
            
                {   
                    'ssh_host':         '192.168.1.21',
                    'ssh_port':         22,
                    'ssh_username':     'dev01',
                    'ssh_password':     '**********',
                    'ssh_pkey':         None,
                    'ssh_pkey_pw':      None,

                    'remote_hostname':  '127.0.0.1',
                    'remote_port':      3306,
                    'local_hostname':   '127.0.0.1',
                    'local_port':       3308
                }
              
            If ssh_password is provided, will use ssh_password;
            If not will use ssh_pkey.
            
            The ``local_port`` is just a temporary port number to connect if 
            it is not used. If already used, will find another port. 
            
                
        """
        
        self.TAG                = 'Model'
        
        self.database_id        = database_id
        
        self.logger             = logger

        self.db_conn            = None
        
        self.models             = {}

        self.credentials        = credentials
        self.ssl                = ssl
        self.tunnel_settings    = tunnel_settings
        
        self.ssh_tunnel         = None
        
        self.local_port_num     = None
        
        
        # disabled autoconnect; must call self.connect_to_db() manually
        #self.connect_to_db()

        
    def append_models(self, model_names):
        """
        Will append models.
        
        Parameters
        ----------
        model_names : list of tuples
            Each of the tuple should be (identifier, class_name)
        
            Example of models
            
            .. code-block:: python
            
               from model.m_stock          import Stock
               from model.m_stock_exchange import StockExchange
               from model.m_stock_index    import StockIndex
               from model.m_system         import System
               
               model_names = [
                   ('stock',               Stock),
                   ('stock_exchange',      StockExchange),
                   ('stock_index',         StockIndex)
               ]
        """
        for model_name in model_names:
            self.models[model_name[0]] = model_name[1](self)


    def __getitem__(self, model_name):
        return self.models[model_name]
            
    
    def is_port_in_use(self, hostname, port):
        """
        Will check if the host port is in use.
        
        Returns
        -------
        bool
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((hostname, port)) == 0
    
    
    def connect_to_db(self):
        """Connects to database."""
        if self.tunnel_settings is None:
            # Case when the application and database server runs on same host
            
            hostname                = self.credentials['db_host']
            port                    = 3306
            database                = self.credentials['database']
            
            try:
                
                if self.ssl is None:
                
                    self.db_conn        = MySQLdb.connect(  
                            host        = hostname,
                            port        = port,
                            
                            user        = self.credentials['db_user'],
                            password    = self.credentials['db_password'], 
                            database    = database, 
                           
                            autocommit  = True)
                
                else:
                    self.db_conn        = MySQLdb.connect(  
                            host        = hostname,
                            port        = port,
                            
                            ssl_mode    = 'VERIFY_IDENTITY',
                       
                            
                            user        = self.credentials['db_user'],
                            password    = self.credentials['db_password'], 
                            database    = database, 
                            
                            autocommit  = True)
                
                            
                self.local_port_num = port
                
                s  = '\nConnected to MySQL\n'
                s += self.get_info_str() + '\n'
                self.logger.append(tag = self.TAG, msg = s)
                
            except Exception as e:
                s  = self.get_info_str() + '\n'
                s += 'Cannot connect to MySQL DB' + str(e)
                self.logger.append(
                        log_level   = LOG_FATAL, 
                        tag         = self.TAG, 
                        msg         = s)
                self.db_conn        = None

        
        else:
            """
            Stop previous ssh_tunnel connection if there is any.
            """
            if self.ssh_tunnel is not None:
                try:
                    self.ssh_tunnel.stop()
                except Exception as e:
                    s = 'Cannot stop SSH tunnel; error\n' + str(e)
                    self.logger.append(tag = self.TAG, msg = s)
                    
                    # continue  below
            
            
            settings        = self.tunnel_settings
            
            """
            The set local_hostname and local port maybe in used;
            If this is in used, will loop for MAX_NUM_LOOK_AVAILABLE_PORT
            to look for available port.
            """
            count           = 0
            local_port_num  = settings['local_port']
            local_hostname  = settings['local_hostname']
            
            found_unused_port = 0
            while count < MAX_NUM_LOOK_AVAILABLE_PORT:
                if self.is_port_in_use(local_hostname, local_port_num) == False:
                    found_unused_port = 1
                    break
                
                local_port_num += 1
                count += 1
            
            
            database        = self.credentials['database']
            
            if found_unused_port == 0:
                values = (local_hostname, settings['local_port'], local_port_num)
                
                s  = '\n\nNo database connection to: %s\n' % database
                s += 'SSH local_bind_address cannot find unused port for '
                s += '%s; from port = %s; to port = %s\n\n' % values
                self.logger.append(tag = self.TAG, msg = s)
                return
            
            
            s  = '\nFound unused port at: %s\n\n' % local_port_num
            self.logger.append(tag = self.TAG, msg = s)
            
            
            ssh_address     = (settings['ssh_host'], settings['ssh_port'])
            remote_address  = (settings['remote_hostname'], settings['remote_port'])
            local_address   = (local_hostname, local_port_num)
            
            self.local_port_num = local_port_num
            
            s  = '\n\nWill use SSH tunnel to access database: %s\n' % database
            s += 'SSH         ip_address: %s; port: %s\n'   % ssh_address
            s += 'Remote bind ip_address: %s; port: %s\n'   % remote_address
            s += 'Local  bind ip_address: %s; port: %s\n\n' % local_address
            self.logger.append(tag = self.TAG, msg = s)
        
        
            """
            These are the logs generated
            
            2023-02-14 10:21:35.834 [DEBUG] Model:
            Found unused port at: 3307


            2023-02-14 10:21:35.834 [DEBUG] Model:

            Will use SSH tunnel to access database: stk_data_us
            SSH         ip_address: 192.168.1.22; port: 22
            Remote bind ip_address: 127.0.0.1; port: 3306
            Local  bind ip_address: 127.0.0.1; port: 3307


            Which corresponds to this open port
            
            dev01@lnx-dev-02:~/cyfi/app/current/scripts$ sudo netstat -tulpn | grep LISTEN
            [sudo] password for dev01:
            tcp        0      0 127.0.0.1:33060         0.0.0.0:*               LISTEN      3400997/mysqld
            tcp        0      0 0.0.0.0:5000            0.0.0.0:*               LISTEN      2583949/python3
            tcp        0      0 0.0.0.0:5001            0.0.0.0:*               LISTEN      2583949/python3
            tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      3400997/mysqld
            tcp        0      0 127.0.0.1:3307          0.0.0.0:*               LISTEN      2583949/python3
            tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      763/systemd-resolve
            tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      952/sshd: /usr/sbin
            tcp6       0      0 :::80                   :::*                    LISTEN      1184568/httpd
            tcp6       0      0 :::22                   :::*                    LISTEN      952/sshd: /usr/sbin

            
            
            """
            
            try:
                
                if 'ssh_pkey_pw' in settings:
                    self.ssh_tunnel = sshtunnel.SSHTunnelForwarder(
                        (settings['ssh_host'], settings['ssh_port']),
                        ssh_username        = settings['ssh_username'],
                        ssh_password        = settings['ssh_password'],
                        ssh_pkey            = settings['ssh_pkey'],
                        ssh_private_key_password = settings['ssh_pkey_pw'],
                        
                        remote_bind_address = remote_address,
                        local_bind_address  = local_address
                    )
                
                else:
                    self.ssh_tunnel = sshtunnel.SSHTunnelForwarder(
                        (settings['ssh_host'], settings['ssh_port']),
                        ssh_username        = settings['ssh_username'],
                        ssh_password        = settings['ssh_password'],
                        ssh_pkey            = settings['ssh_pkey'],
                        
                        remote_bind_address = remote_address,
                        local_bind_address  = local_address
                    )
                
                self.ssh_tunnel.start()
            
            except Exception as e:
                s = 'Cannot start SSH tunnel; error\n' + str(e)
                self.logger.append(tag = self.TAG, msg = s)
                return
            
            
            hostname            = settings['local_hostname']
            port                = local_port_num
            
            try:
                self.db_conn    = MySQLdb.connect(  
                    host        = hostname,
                    port        = port,
                    
                    user        = self.credentials['db_user'],
                    password    = self.credentials['db_password'], 
                    database    = database,
                     
                    charset     = 'utf8',
                    autocommit  = True)
                    
                values = (hostname, port, database)
                s = '\nConnected to MySQL at %s:%s; db: %s\n' % values
                self.logger.append(tag = self.TAG, msg = s)
            
            except Exception as e:
                s  = self.get_info_str() + '\n'
                s += 'Cannot connect to MySQL DB' + str(e)
                self.logger.append(
                        log_level   = LOG_FATAL, 
                        tag         = self.TAG, 
                        msg         = s)
                self.db_conn        = None
            

    def check_if_connected(self):
        """ 
        Will check if still connected to MySQL. 

        To prevent multiple connections this must be checked before doing 
        connecting to the database.
        
        Returns
        -------
        bool
        """

        if self.db_conn is not None:
            try:
                self.db_conn.ping()
                return True
            except Exception as e:
                self.db_conn = None
            
        return False


    def disconnect_db(self):
        self.db_conn.close()
        
        if self.ssh_tunnel is not None:
            try:
                self.ssh_tunnel.stop()
                self.ssh_tunnel = None
                
            except Exception as e:
                s = 'Cannot stop SSH tunnel; error\n' + str(e)
                self.logger.append(tag = self.TAG, msg = s)
                return
        
        self.db_conn = None
        
        
    def execute_sql(self, sql = None):
        """
        Generic execute SQL. Will not return any SELECT.
        
        Parameters
        ----------
        sql : string
            SQL to be executed
        
        """
        
        
        # Check if still connected to database
        if self.check_if_connected() == False:
            # Make new connection
            self.connect_to_db()

        # Get database connection
        conn = self.db_conn
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            cursor.close()

        except Exception as e:
            msg = 'execute_sql(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            
            return False
        
        return True

    
    def get_short_info(self):
        """
        Get database short information.
        
        Returns
        -------
        dictionary
            Will return a dictionary similar to this ::
            
              {
                  'db_location':  'localhost',
                  'db_name':      'cyfi'
              }
              
              or
              
              {
                  'db_location':  '192.168.1.21:22',
                  'db_name':      'cyfi'
              }
            
        """
        
        db_location         = 'localhost'
        if self.tunnel_settings is not None:
            ssh_host        = self.tunnel_settings['ssh_host']
            ssh_port        = self.tunnel_settings['ssh_port']
            db_location     = ssh_host + ':' + str(ssh_port)
        
        result = {
            'db_location':  db_location,
            'db_name':      self.credentials['database']
        }
        
        return result
        

    def get_info_str(self):
        """
        Will return database info.
        
        Returns : string
            Will return a string similar to this ::
            
                Database Location: remote
                =================================
                ssh_host:          192.168.1.21
                ssh_port:          22
                ssh_username:      cyfi-bkops
                ssh_password:        
                  
                remote_hostname:   127.0.0.1
                remote_port:       3306

                Database id:       1
                Database name:     cyfi
                Database user:     cyfi-bkops
              
        """
        s  = '\n'
        
        tunnel_settings = self.tunnel_settings
        credentials     = self.credentials
        
        if tunnel_settings is not None:
            values = 'remote'
        else:
            values = self.credentials['db_host']
        
        s += 'Database Location: %s\n' % values
            
        
        if self.tunnel_settings is not None:
            s += '=================================\n'
            s += 'ssh_host:          %s\n' % tunnel_settings['ssh_host']
            s += 'ssh_port:          %s\n' % tunnel_settings['ssh_port']
            s += 'ssh_username:      %s\n' % tunnel_settings['ssh_username']
            s += 'ssh_password:        \n' 
                
            s += 'remote_hostname:   %s\n' % tunnel_settings['remote_hostname']
            s += 'remote_port:       %s\n' % tunnel_settings['remote_port']
            s += 'local_port:        %s\n' % self.local_port_num
        
        
        s += '\n'
        s += 'Database id:       %s\n' % self.database_id 
        s += 'Database name:     %s\n' % credentials['database']
        s += 'Database user:     %s\n' % credentials['db_user']
        
        return s
        
        
        
def get_database_model(logger, host_ip_address, db_access, model_names):
    """
    Will create a Model object.
    
    Parameters
    ----------
    
    logger : common.commmon_logger.Logger object
    
    host_ip_address : string
    
    db_access : dictionary
        The structure should be similar to this ::
        
            {
                'database_id':      1,

                'db_location': {
                    'ip_address':   '',
                    'ssh_user':     '',
                    'ssh_pw':       '',
                    'ssh_port':     '',
                    'database':     ''
                },

                'db_user'
                    'user':         '',
                    'pw':           ''
                }
            }

    model_names : list of tuples
        Each of the tuple should be (identifier, class_name)
        
    Returns
    -------
    Model object
        Will return the created Model object.
        
    """
    
    database_id     = 0
    db_location     = db_access['db_location']
    db_user         = db_access['db_user']
    
    ssh_tunnel_settings = None

    if 'database_id' in db_access:
        database_id = db_access['database_id']


    if db_location['ip_address'] != host_ip_address:
        
        """
        The remote_port is always fixed. The set local_port is the 
        starting port number where to look for available port.
        The Model object should dynamically look for another port 
        in case this local_port is already used. 
        """
        ssh_tunnel_settings = {   
            'ssh_host':         db_location['ip_address'],
            'ssh_port':         int(db_location['ssh_port']),
            'ssh_username':     db_location['ssh_user'],
            'ssh_password':     db_location['ssh_pw'],
            'ssh_pkey':         None,
            
            'remote_hostname':  '127.0.0.1',
            'remote_port':      3306,
            'local_hostname':   '127.0.0.1',
            'local_port':       3307
        }

        
    credentials = {
        'db_host':          'localhost',
        'db_user':          db_user['user'],
        'db_password':      db_user['pw'],
        'database':         db_location['database']
    }


    m = Model(
            database_id     = database_id,
            logger          = logger, 
            credentials     = credentials, 
            tunnel_settings = ssh_tunnel_settings)
    
    if model_names is not None:
        m.append_models(model_names)
   
    
    return m

