# September 23, 2025
# Jack Wong

from common_constants       import *


class ProductionGroup:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'ProductionGroup'


    def create(self, data = None):
        """
        PROCEDURE production_group_create(
            in_user_id              INT,

            in_pig_prod_id          INT, /*initial pig_production in the production_group*/
            
            in_date_added           INT
        )  
        """
        
        sql =  'CALL production_group_create('
        sql += '%s,'    % data.user_id
        
        sql += '%s,'    % data.pig_prod_id
        sql += '"%s");' % data.date_added
        
        
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
                
                'production_group': {
                    'id':               row[3]
                }
            }

        return None
    
    


    def get_list(self):
        """
        Will get pig_race list.
        
        
        Returns
        -------
        list of dictionary

        """
        
                   
        sql =   """
                SELECT 
                    id,
                    name
                FROM pig_race
                """ 
        
        
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
                cur_entry = {
                    'id':               row[0], 
                    'name':             row[1]
                }
                
                result.append(cur_entry)

        
        return result
    
    