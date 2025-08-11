# January 3, 2024
# Jack Wong

from common_constants       import *


class Account:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'Account'

    
    def register(self, data = None):
        """
        PROCEDURE account_register(
            in_user_id              INT,
    
            in_name                 VARCHAR(100)
        )  
        """
        
        user_id         = data['user_id']
        name            = data['name']
        
        sql =  'CALL account_register('
        sql += '%s,'    % user_id
        sql += '"%s");' % name
        
        
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        row = None

        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            row = cursor.fetchone()
            cursor.close()

        except Exception as e:
            msg = 'register(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'account': {
                    'id':               row[3],
                    'name':             row[4],
                    'flag':             row[5],
                    'status':           row[6],
                    'dt_trial_start':   row[7],
                    'dt_trial_end':     row[8]
                }
            }

        return None

    
    def update_hashid(self, data = None):
        account_id      = data['account_id']
        hashid          = data['hashid']
        
        values = (hashid, account_id)
        
        sql =   """
                UPDATE account SET
                    hashid    = "%s"
                WHERE id = %s;
                """ % values
        
        return self.model.execute_sql(sql)
    
    
    def update(self, data = None):
        """
        PROCEDURE account_update(
            in_user_id              INT,
    
            in_name                 VARCHAR(100)
        )  
        """
        
        user_id         = data['user_id']
        name            = data['name']
        
        sql =  'CALL account_update('
        sql += '%s,'    % user_id
        sql += '"%s");' % name
        
        
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        row = None

        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            row = cursor.fetchone()
            cursor.close()

        except Exception as e:
            msg = 'update(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'account': {
                    'id':               row[3],
                    'name':             row[4],
                    'flag':             row[5],
                    'status':           row[6],
                    'dt_trial_start':   row[7],
                    'dt_trial_end':     row[8]
                }
            }

        return None

    
    def add_account_request_add_user(self, data = None):
        """
        PROCEDURE account_request_user_add(
            in_account_id               INT,
            in_user_id                  INT,
            
            in_user_hashid              VARCHAR(10)
            
        )
        """
        
        user_id         = data['user_id']
        account_id      = data['account_id']
        user_hashid     = data['user_hashid']
        
        values = (user_id, account_id, user_hashid)
        
        sql =  'CALL account_request_user_add('
        sql += '%s,'    % account_id
        sql += '%s,'    % user_id
        sql += '"%s");' % user_hashid
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        row = None

        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            row = cursor.fetchone()
            cursor.close()

        except Exception as e:
            msg = 'register(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'account': {
                    'id':               row[3],
                    'name':             row[4],
                    'flag':             row[5],
                    'status':           row[6]
                },
                
                'user': {
                    'id':               user_id,
                    'email':            row[7]
                }
            }

        return None
        
        
    def approve_account_request_add_user(self, data = None):
        """
        PROCEDURE account_request_user_add_approve(
            in_acc_req_add_id           INT,
            in_user_id                  INT
            
        )
        """
        
        user_id         = data['user_id']
        acc_req_add_id  = data['acc_req_add_id']
        
        values = (acc_req_add_id, user_id)
        
        
        sql =  'CALL account_request_user_add_approve('
        sql += '%s,'    % acc_req_add_id
        sql += '%s);'   % user_id
        
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        row = None

        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            row = cursor.fetchone()
            cursor.close()

        except Exception as e:
            msg = 'register(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'account': {
                    'id':               row[3],
                    'name':             row[4],
                    'flag':             row[5],
                    'status':           row[6]
                },
                
                'user': {
                    'id':               user_id,
                    'email':            row[7]
                }
            }

        return None

