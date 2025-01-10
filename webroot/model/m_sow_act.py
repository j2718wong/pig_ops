# December 13, 2024
# Jack Wong

from common_constants       import *



class SowActivity:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'SowActivity'
    
    
    def get_latest_sow_activities(self, full_info = 0, list_ai_id = None):
        """
        Will get list of latest sow activities.
        
        
        Returns
        -------
        list of dictionary

        """
        
        s_list_ai_id = ''
        if list_ai_id is not None:
            s_list_ai_id = ','.join(list_ai_id)
            s_list_ai_id = ' AND ai_id IN(' + s_list_ai_id + ')'
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        if full_info == 0:
            sql =   """
                    SELECT 
                        a.id,
                        a.ai_id,
                        a.sow_number,
                        b.description AS activity,
                        a.date,
                        a.date_2,
                        a.days_since_ai,
                        a.description

                    FROM sow_coming_activity a
                    LEFT OUTER JOIN coming_activity b           ON a.coming_activity_id = b.id
                    LEFT OUTER JOIN artificial_insemination c   ON a.ai_id = c.id
                    WHERE c.status_id IN (1,4) AND (
                        (a.date >= CURRENT_DATE AND a.date_2 IS NULL) OR 
                        (a.date <= CURRENT_DATE AND CURRENT_DATE <= a.date_2)
                    ) %s
                    ORDER BY a.sow_number, a.id;
                    """ % s_list_ai_id
        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.ai_id,
                        a.sow_number,
                        b.description AS activity,
                        a.date,
                        a.date_2,
                        a.days_since_ai,
                        a.description

                    FROM sow_coming_activity a
                    LEFT OUTER JOIN coming_activity b           ON a.coming_activity_id = b.id
                    LEFT OUTER JOIN artificial_insemination c   ON a.ai_id = c.id
                    WHERE c.status_id IN (1,4) %s
                    ORDER BY a.sow_number, a.id;
                    """ % s_list_ai_id

        
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            
        except Exception as e:
            msg = 'get_latest_sow_activities(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            last_sow_number = None
            
            for row in rows:
                cur_id                  = row[0]
                cur_ai_id               = row[1]
                cur_sow_number          = row[2]
                cur_activity            = row[3]
                cur_date                = str(row[4])
                
                cur_date_2              = None
                if row[5] is not None:
                    cur_date_2          = str(row[5])
                
                cur_days_since_ai       = None
                if row[6] is not None:
                    cur_days_since_ai   = row[6]
                    
                cur_description         = ''
                if row[7] is not None:
                    cur_description     = row[7]
                
                
                if last_sow_number is None or last_sow_number != cur_sow_number:
                
                    cur_entry = {
                        'ai_id':            cur_ai_id,
                        'sow_number':       cur_sow_number,
                        
                        'activities':       []
                    }
                    
                    result.append(cur_entry) 
                    
                    last_sow_number = cur_sow_number
                
                
                cur_activity = {
                   'id':            cur_id,
                   'date':          cur_date,
                   'date_2':        cur_date_2,
                   'days_ai':       cur_days_since_ai,
                   'activity':      cur_activity,
                   'desc':          cur_description
                }
                
                cur_entry['activities'].append(cur_activity)

        
        return result
    
  
    def get_latest_calendar_activities(self, date_start, date_end):
        """
        Will get list of latest calendar activities.
        
        
        Returns
        -------
        list of dictionary

        """
        
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
      
        sql =   """
                SELECT 
                    a.id,
                    a.ai_id,
                    a.sow_number,
                    b.description AS activity,
                    a.date,
                    a.date_2,
                    a.days_since_ai,
                    a.description

                FROM sow_coming_activity a
                LEFT OUTER JOIN coming_activity b           ON a.coming_activity_id = b.id
                LEFT OUTER JOIN artificial_insemination c   ON a.ai_id = c.id
                WHERE c.status_id IN (1,4) AND (
                    (a.date >= '%s' AND a.date <= '%s')
                )
                ORDER BY a.date, a.sow_number;
                """ % (date_start, date_end)
    
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            
        except Exception as e:
            msg = 'get_latest_calendar_activities(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            last_date = None
            
            for row in rows:
                cur_id                  = row[0]
                cur_ai_id               = row[1]
                cur_sow_number          = row[2]
                cur_activity            = row[3]
                cur_date                = str(row[4])
                
                cur_date_2              = None
                if row[5] is not None:
                    cur_date_2          = str(row[5])
                
                cur_days_since_ai       = None
                if row[6] is not None:
                    cur_days_since_ai   = row[6]
                    
                cur_description         = ''
                if row[7] is not None:
                    cur_description     = row[7]
                
                
                if last_date is None or last_date != cur_date:
                
                    cur_entry = {
                        'date':             cur_date,
                        
                        'activities':       []
                    }
                    
                    result.append(cur_entry) 
                    
                    last_date = cur_date
                
                
                cur_activity = {
                   'ai_id':         cur_ai_id,
                   'sow_number':    cur_sow_number, 
                   'id':            cur_id,
                   'days_ai':       cur_days_since_ai,
                   'activity':      cur_activity,
                   'desc':          cur_description
                }
                
                cur_entry['activities'].append(cur_activity)

        
        return result
    
    
    def get_ai_list(self):
        """
        Will get list of latest calendar activities.
        
        
        Returns
        -------
        list of dictionary

        """
        
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
      
        sql =   """
                SELECT 
                    a.id,
                    a.sow_number,
                    a.date_ai,
                    a.date_actual_birth,
                    a.num_days_since_ai,
                    b.name,
                    
                    a.num_piglets_dead_at_birth,
                    a.num_piglets_live_male,
                    a.num_piglets_live_female,
                    a.num_piglets_weaning_male,
                    a.num_piglets_weaning_female

                FROM artificial_insemination a
                LEFT OUTER JOIN ai_status b           ON a.status_id = b.id
                ORDER BY a.sow_number ASC, a.id DESC
                """ 
    
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            
        except Exception as e:
            msg = 'get_ai_list(); error in executing query[] = ' + sql
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
                cur_sow_number          = row[1]
                cur_date_ai             = str(row[2])
                
                cur_date_actual         = None
                if row[3] is not None:
                    cur_date_actual     = str(row[3])
                
                cur_days_since_ai       = None
                if row[4] is not None:
                    cur_days_since_ai   = row[4]
                    
                cur_status              = row[5]
                    
                cur_num_b_dead          = None
                if row[6] is not None:
                    cur_num_b_dead      = row[6]
                
                cur_num_b_male          = None
                if row[7] is not None:
                    cur_num_b_male      = row[7]
                
                cur_num_b_female        = None
                if row[8] is not None:
                    cur_num_b_female    = row[8]
                    
                cur_num_w_male          = None
                if row[9] is not None:
                    cur_num_w_male      = row[9]
                
                cur_num_w_female        = None
                if row[10] is not None:
                    cur_num_w_female    = row[10]
                
                cur_num_w_dead          = None
                if cur_num_w_male is not None and cur_num_w_female is not None:
                    cur_num_w_dead = cur_num_b_male + cur_num_b_female - \
                                        cur_num_w_male - cur_num_w_female
                
                cur_entry = {
                    'id':               cur_id,
                    'sow_number':       cur_sow_number, 
                    'date_ai':          cur_date_ai,
                    'date_actual_birth': cur_date_actual,
                    'days_ai':          cur_days_since_ai,
                    'status':           cur_status,
                   
                    'num_piglets_birth':{
                        'dead':         cur_num_b_dead, 
                        'male':         cur_num_b_male,
                        'female':       cur_num_b_female
                    },
                    
                    'num_piglets_weaning':{
                        'dead':         cur_num_w_dead, 
                        'male':         cur_num_w_male,
                        'female':       cur_num_w_female
                    }
                   
                }
                
                result.append(cur_entry)

        
        return result
    
    
    
    
    