# August 23, 2025
# Jack Wong

from common_constants       import *


class PigRace:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'PigRace'


    def get_pig_race_list(self):
        """
        Will get pig_race list.
        
        
        Returns
        -------
        list of dictionary

        """
        
                   
        sql =   """
                SELECT 
                    id
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
            conn.close()
            
        except Exception as e:
            msg = 'get_pig_race_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            
            for row in rows:
                cur_pig_race_id         = row[0]
                cur_pig_race_name       = row[1]
               
                cur_entry = {
                    'id':               cur_pig_race_id, 
                    'name':             cur_pig_race_name
                }
                
                result.append(cur_entry)

        
        return result
    
    