# January 3, 2024
# Jack Wong

from common_constants       import *


class AccountRequest:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'AccountRequest'


    def add_user(self, data = None):
        """
        PROCEDURE account_request_user_add(
            in_account_id               INT,
            in_user_id                  INT
            
        )
        """
        
        user_id         = data['user_id']
        account_id      = data['account_id']
                
        values = (user_id, account_id)
        
        sql =  'CALL account_request_user_add('
        sql += '%s,'    % account_id
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
            msg = 'add_user(); error in executing query[] = ' + sql
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
                
                'account_request': {
                    'id':               row[7]
                },
                
                'user': {
                    'id':               user_id,
                    'email':            row[8]
                }
            }

        return None
        
        
    def approve_add_user(self, data = None):
        """
        PROCEDURE account_request_user_add_approve(
            in_account_request_id       INT,
            in_approving_user_id        INT
        )
        """
        
        acc_request_id      = data['acc_request_id']
        approving_user_id   = data['approving_user_id']
        
        
        values = (acc_request_id, approving_user_id)
        
        
        sql =  'CALL account_request_user_add_approve('
        sql += '%s,'    % acc_request_id
        sql += '%s);'   % approving_user_id
        
        
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
            msg = 'approve_add_user(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            row = None

        if row is not None:
            
            cur_dt_approved = str(row[8]) if row[8] else None
            
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'account_request': {
                    'id':               row[3],
                    'status':           row[4],
                    
                    'approving_user':{
                        'username':     row[5],
                        'name_last':    row[6],
                        'name_first':   row[7]
                    },
                    
                    'dt_approved':      cur_dt_approved
                },
                
                'requesting_user': {
                    'id':               row[8],
                    'email':            row[9]
                }
            }

        return None

