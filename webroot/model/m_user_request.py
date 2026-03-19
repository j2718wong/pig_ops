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
            in_access_code_id           INT,
            in_requesting_user_id       INT          
        )
        """
        
        access_code_id  = data['access_code_id']
        user_id         = data['user_id']
                
        
        sql =  'CALL user_request_join_account('
        sql += '%s,'    % access_code_id
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
                
                'user': {
                    'account_id':       row[3],
                    'email':            row[4]
                }
            }

        return None
        
        
    def approve_join_account(self, data = None):
        """
        PROCEDURE user_request_join_account_approve(
            in_approving_user_id        INT,
            
            in_user_request_id          INT,
            in_user_group_num           INT,
            
            in_is_approved              INT,
            
            in_pig_farm_id              INT
            
        )
        """
        
        sql =  'CALL user_request_join_account_approve('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.user_req_id
        sql += '%s,'    % data.group_num
        
        sql += '%s,'    % data.is_approved
        
        sql += '%s);'   % data.pig_farm_id

        
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
                        'email':        row[5],
                        'name_last':    row[6],
                        'name_first':   row[7]
                    },
                    
                    'dt_approved':      str(row[8]) if row[8] else None,
                },
                
                'requesting_user': {
                    'id':               row[9],
                    'email':            row[10]
                }
            }

        return None


    def get_list(self, account_id):
        
        
        sql =   """
                SELECT 
                    a.id,
                    a.status_id,
                    
                    b.name_last,
                    b.name_first,
                    b.email,
                    
                    a.dt_entry
                    
                FROM user_request a 
                LEFT OUTER JOIN user b        ON a.requesting_user_id   = b.id
                WHERE a.account_id = %s AND a.status_id = 1 
                ORDER BY a.dt_entry DESC
                """ % account_id
        
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()
            #conn.close()
            
        except Exception as e:
            msg = 'get_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        
        result = []
        if rows is not None:
            
            for row in rows:
                cur_id                  = row[0]
                cur_status_id           = row[1]

                
                cur_name_last           = row[2]
                cur_name_first          = row[3]
                cur_email               = row[4]
                
                cur_dt_entry            = str(row[5])[0:10]
                
                cur_entry = {
                    'user_req': {
                        'id':           cur_id,
                        'status_id':    cur_status_id,
                        'dt_entry':     cur_dt_entry
                    },
                    
                    'requesting_user': {
                        'name_last':    cur_name_last,
                        'name_first':   cur_name_first,
                        'email':        cur_email
                    }
                    
                }
                
                    
                result.append(cur_entry)
        
        return result
    
