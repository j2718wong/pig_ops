# January 14, 2026
# Jack Wong

from common_constants       import *



class AccountMedVac:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'AccountMedVac'


    def add(self, data = None):
        """
        PROCEDURE account_medvac_add(
            in_user_id              INT,
            
            in_medvac_name          VARCHAR(50)
        )  
        """
        
        sql =  'CALL account_medvac_add('
        sql += '%s,'    % data.user_id
        sql += '"%s")'  % data.name
        
        
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
            msg = 'add(); error in executing query[] = ' + sql
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
                
                'account_medvac': {
                    'id':               row[3]
                }
            }

        return None
    
    
    def update(self, data = None):
        """
        PROCEDURE account_pig_ops_update(
            in_user_id              INT,
    
            in_account_pig_ops_id   INT,
            in_num_days_since       INT,
            
            is_medvac               INT,
            
            in_name                 VARCHAR(50),
            in_short_name           VARCHAR(15),
            in_description          VARCHAR(160)
        )
        """
       
        sql =  'CALL account_pig_ops_update('
        sql += '%s,'    % data.user_id
        sql += '%s,'    % data.account_pig_ops_id
        sql += '%s,'    % data.num_days_since
        sql += '%s,'    % data.is_medvac
        
        sql += '"%s",'  % data.name
        
        if data.short_name is not None and len(data.short_name) > 0:
            sql += '"%s",'   % data.short_name
        else:
            sql += 'NULL,'
        
        if data.description is not None:
            sql += '"%s");'   % data.description
        else:
            sql += 'NULL);'
        
        
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
                
                'account_pig_ops': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def delete(self, data = None):
        user_id             = data['user_id']
        account_pig_ops_id  = data['account_pig_ops_id']
        
        """
        PROCEDURE account_pig_ops_delete(
            in_user_id                  INT,
            
            in_account_pig_ops_id     INT
        )
        """
       
        sql =  'CALL account_pig_ops_delete('
        sql += '%s,'    % user_id
        sql += '%s);'   % account_pig_ops_id
        
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
            msg = 'delete(); error in executing query[] = ' + sql
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
                
                'account_pig_ops': {
                    'id':               row[3],
                    'flag':             row[4],
                    'name':             row[5]
                }
            }

        return None
    
    
    def get_list(self, account_id, inc_deleted = 0, inc_user_audit = 0):
        
        where_clause = 'WHERE account_id = %s ' %account_id
            
        if inc_deleted == 0:
            where_clause += ' AND (a.flag & 1) = 0' 
            
        
        if inc_user_audit == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.name
                    FROM account_medvac a
                    %s
                    ORDER BY a.name
                    """ % (where_clause)
        else:
            
            sql =   """
                    SELECT 
                        a.id,
                        a.name
                    
                        
                        c.name_last,
                        c.name_first,
                        a.dt_entry,
                        
                        d.name_last,
                        d.name_first,
                        a.dt_last_update
                        
                    FROM account_medvac a
                    LEFT OUTER JOIN user c          ON a.added_by_user_id   = c.id
                    LEFT OUTER JOIN user d          ON a.last_update_user_id = d.id
                    %s
                    ORDER BY a.name
                    """ % where_clause

        
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
                    
                
                if inc_user_audit == 0:
                    
                    cur_entry = {
                        'acc_medvac': {
                            'id':               row[0],
                            'name':             row[1]
                        }
                    }
                
                else:
                    
                    cur_entry = {
                        'acc_medvac': {
                            'id':               row[0],
                            'name':             row[1]
                        },
                        
                        'added_by': {
                            'name_last':        row[2],
                            'name_first':       row[3]
                        },
                        
                        'last_update':{
                            'name_last':        row[4],
                            'name_first':       row[5]
                        }
                    }
                    
                result.append(cur_entry)
        
        return result
    
    