# January 3, 2024
# Jack Wong

from common_constants       import *


class UserRequest:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'UserRequest'


    def join_account(self, data = None):
        """
        PROCEDURE user_request_join_account(
            in_account_id               INT,
            in_user_id                  INT
            
        )
        """
        
        account_id      = data['account_id']
        user_id         = data['user_id']
                
        values = (user_id, account_id)
        
        sql =  'CALL user_request_join_account('
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
            msg = 'join_account(); error in executing query[] = ' + sql
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
                
                'user_request': {
                    'id':               row[3],
                    'status_id':        row[4]
                }
            }

        return None
        
        
    def approve_join_account(self, data = None):
        """
        PROCEDURE user_request_join_account_approve(
            in_user_request_id          INT,
            in_approving_user_id        INT,
            in_assigned_user_group_id   INT
        )
        """
        
        user_request_id     = data['user_request_id']
        approving_user_id   = data['approving_user_id']
        user_group_id       = data['user_group_id']
        
        
        
        sql =  'CALL user_request_join_account_approve('
        sql += '%s,'    % user_request_id
        sql += '%s,'    % approving_user_id
        sql += '%s);'   % user_group_id
        
        
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
            msg = 'approve_join_account(); error in executing query[] = ' + sql
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
                
                'user_request': {
                    'id':               row[3],
                    'status_id':        row[4],
                    
                    'approving_user':{
                        'email':        row[6],
                        'name_last':    row[7],
                        'name_first':   row[8]
                    },
                    
                    'dt_approved':      str(row[9]) if row[9] else None,
                },
                
                'requesting_user': {
                    'id':               row[10],
                    'email':            row[11]
                }
            }

        return None

