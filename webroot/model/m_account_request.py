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
                
                'user': {
                    'id':               user_id,
                    'email':            row[7]
                }
            }

        return None
        
        
    def approve_add_user(self, data = None):
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
            msg = 'approve_add_user(); error in executing query[] = ' + sql
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

