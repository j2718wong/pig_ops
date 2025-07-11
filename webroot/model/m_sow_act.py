# December 13, 2024
# Jack Wong

from common_constants       import *



class SowActivity:
    def __init__(self, model):
        self.model              = model
        self.TAG                = 'SowActivity'
    
    
    def get_latest_sow_activities(self, full_info = 0, list_ins_id = None):
        """
        Will get list of latest sow activities.
        
        
        Returns
        -------
        list of dictionary

        """
        
        s_list_ins_id = ''
        if list_ins_id is not None:
            s_list_ins_id = ','.join(list_ins_id)
            s_list_ins_id = ' AND insemination_id IN(' + s_list_ins_id + ')'
        
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
                        a.insemination_id,
                        a.sow_number,
                        b.description AS activity,
                        a.date,
                        a.date_2,
                        a.days_since_ins,
                        a.description

                    FROM sow_coming_activity a
                    LEFT OUTER JOIN coming_activity b  ON a.coming_activity_id = b.id
                    LEFT OUTER JOIN pig_production c   ON a.insemination_id = c.id
                    WHERE c.status_id IN (1,4) AND (
                        (a.date >= CURRENT_DATE AND a.date_2 IS NULL) OR 
                        (a.date <= CURRENT_DATE AND CURRENT_DATE <= a.date_2)
                    ) %s
                    ORDER BY a.sow_number, a.id;
                    """ % s_list_ins_id
        else:
            sql =   """
                    SELECT 
                        a.id,
                        a.insemination_id,
                        a.sow_number,
                        b.description AS activity,
                        a.date,
                        a.date_2,
                        a.days_since_ins,
                        a.description

                    FROM sow_coming_activity a
                    LEFT OUTER JOIN coming_activity b           ON a.coming_activity_id = b.id
                    LEFT OUTER JOIN pig_production c   ON a.insemination_id = c.id
                    WHERE c.status_id IN (1,4) %s
                    ORDER BY a.sow_number, a.id;
                    """ % s_list_ins_id

        
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()
            
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
                cur_ins_id              = row[1]
                cur_sow_number          = row[2]
                cur_activity            = row[3]
                cur_date                = str(row[4])
                
                cur_date_2              = None
                if row[5] is not None:
                    cur_date_2          = str(row[5])
                
                cur_days_since_ins      = None
                if row[6] is not None:
                    cur_days_since_ins  = row[6]
                    
                cur_description         = ''
                if row[7] is not None:
                    cur_description     = row[7]
                
                
                if last_sow_number is None or last_sow_number != cur_sow_number:
                
                    cur_entry = {
                        'ins_id':           cur_ins_id,
                        'sow_number':       cur_sow_number,
                        
                        'activities':       []
                    }
                    
                    result.append(cur_entry) 
                    
                    last_sow_number = cur_sow_number
                
                
                cur_activity = {
                   'id':            cur_id,
                   'date':          cur_date,
                   'date_2':        cur_date_2,
                   'days_ins':      cur_days_since_ins,
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
                    a.insemination_id,
                    a.sow_number,
                    b.description AS activity,
                    a.date,
                    a.date_2,
                    a.days_since_ins,
                    a.description

                FROM sow_coming_activity a
                LEFT OUTER JOIN coming_activity b  ON a.coming_activity_id = b.id
                LEFT OUTER JOIN pig_production c   ON a.insemination_id = c.id
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
                cur_ins_id              = row[1]
                cur_sow_number          = row[2]
                cur_activity            = row[3]
                cur_date                = str(row[4])
                
                cur_date_2              = None
                if row[5] is not None:
                    cur_date_2          = str(row[5])
                
                cur_days_since_ins       = None
                if row[6] is not None:
                    cur_days_since_ins   = row[6]
                    
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
                   'ins_id':        cur_ins_id,
                   'sow_number':    cur_sow_number, 
                   'id':            cur_id,
                   'days_ins':      cur_days_since_ins,
                   'activity':      cur_activity,
                   'desc':          cur_description
                }
                
                cur_entry['activities'].append(cur_activity)

        
        return result
    
    
    def get_pig_prod_list(self, is_active = 0, is_completed = 0, year = None, 
            sow = None):
        """
        Will get list of pig production list.
        
        Parameters
        ----------
        is_active : int
            if > 0, pig production with status gestating, lactating and weaning 
               will be returned
            
  
        is_completed : int
            if > 0, pig production with status Completed will be returned
            
       
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
        
        where_clause    = ''
        order_by        = ' a.sow_number ASC, a.id DESC'
        
        if sow is not None:
            where_clause = "WHERE a.sow_number = '%s'" % sow
            
        else:
            if is_completed > 0:
                where_clause = 'WHERE a.status_id = 7'
                if year is not None:
                    where_clause += ' AND YEAR(a.date_weaning) =  %s' % year
                
            else:
               
                if is_active > 0:
                    where_clause = 'WHERE status_id IN(1,4,5) '
                    if year is not None:
                        where_clause += ' AND YEAR(a.date_insemination) =  %s' % year
                        
                    order_by        = 'a.date_expected_birth '
        
        sql =   """
                SELECT 
                    a.id,
                    a.sow_number,
                    a.date_insemination,
                    a.date_expected_birth,
                    a.date_actual_birth,
                    a.num_days_actual,
                    a.status_id,
                    a.semen_desc,
                    b.name,
                    
                    a.num_piglets_dead_at_birth,
                    a.num_piglets_live_male,
                    a.num_piglets_live_female,
                    a.num_piglets_weaning_male,
                    a.num_piglets_weaning_female,
                    
                    a.date_weaning
         
                FROM pig_production a
                LEFT OUTER JOIN insemination_status b           ON a.status_id = b.id
                %s
                ORDER BY %s
                """ % (where_clause, order_by)
    
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()

        except Exception as e:
            msg = 'get_pig_prod_list(); error in executing query[] = ' + sql
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
                cur_date_insemination   = str(row[2])
                cur_date_expected       = str(row[3])
                
                cur_date_actual         = None
                if row[4] is not None:
                    cur_date_actual     = str(row[4])
                
                cur_num_days_actual     = None
                if row[5] is not None:
                    cur_num_days_actual = row[5]
                    
                cur_status_id           = row[6]
                cur_semen_desc          = row[7]
                cur_status              = row[8]
                    
                cur_num_b_dead          = None
                if row[9] is not None:
                    cur_num_b_dead      = row[9]
                
                cur_num_b_male          = None
                if row[10] is not None:
                    cur_num_b_male      = row[10]
                
                cur_num_b_female        = None
                if row[11] is not None:
                    cur_num_b_female    = row[11]
                    
                cur_num_w_male          = None
                if row[12] is not None:
                    cur_num_w_male      = row[12]
                
                cur_num_w_female        = None
                if row[13] is not None:
                    cur_num_w_female    = row[13]
                
                cur_num_w_dead          = None
                if cur_num_w_male is not None and cur_num_w_female is not None:
                    cur_num_w_dead = cur_num_b_male + cur_num_b_female - \
                                        cur_num_w_male - cur_num_w_female
                                        
                                        
                cur_date_weaning        = None
                if row[14] is not None:
                    cur_date_weaning    = str(row[14])
                
                
                cur_entry = {
                    'id':               cur_id,
                    'sow_number':       cur_sow_number, 
                    'date_ins':         cur_date_insemination,
                    'date_expected':    cur_date_expected,
                    'date_actual_birth': cur_date_actual,
                    'days_actual':      cur_num_days_actual,
                    'status_id':        cur_status_id,
                    'status':           cur_status,
                    'semen_desc':       cur_semen_desc,
                    'date_weaning':     cur_date_weaning,
                   
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
    
    
    def get_sow_list(self, list_sow_numbers = None):
        """
        Will get sow list.
        
        
        Returns
        -------
        list of dictionary

        """
        
        where_clause = ''
        if list_sow_numbers is not None:
            s = ''
            count = 0
            for cur_entry in list_sow_numbers:
                if count > 0: 
                    s += ','
                
                s += f"'{cur_entry}'"
                
            where_clause = ' WHERE sow_number IN (%s) ' %s
        
        
        sql =   """
                SELECT 
                    a.sow_number,
                    a.flag,
                    b.name,
                    a.date_of_birth,
                    a.date_culled,
                    a.comment
                FROM sow a
                LEFT OUTER JOIN sow_status b ON a.sow_status_id = b.id
                %s
                ORDER BY date_of_birth DESC
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
            conn.close()
            
        except Exception as e:
            msg = 'get_sow_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            
            for row in rows:
                cur_sow_number          = row[0]
                cur_flag                = row[1]
                cur_status              = row[2]
                cur_date_of_birth       = str(row[3])
                    
                cur_date_culled         = None
                if row[4] is not None:
                    cur_date_culled     = str(row[4])
                
                cur_comment             = None
                if row[5] is not None:
                    cur_comment         = row[5]
                
                cur_entry = {
                    'sow_number':       cur_sow_number, 
                    'flag':             cur_flag,
                    'status':           cur_status,
                    'date_of_birth':    cur_date_of_birth,
                    'date_culled':      cur_date_culled,
                    'comment':          cur_comment
                }
                
                result.append(cur_entry)

        
        return result
    
    
    def get_sow_farrowing_list(self):
        """
        Will get list of latest sow_farrowing list.
        
        
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
                    a.ins_id,
                    b.sow_number,
                    b.date_actual_birth,
                    b.num_days_since_ai,
                    
                    a.date_start_night_support,
                    a.date_stop_night_support
                    
                FROM sow_farrowing a
                LEFT OUTER JOIN artificial_insemination b  ON a.ins_id = b.id
                ORDER BY a.ins_id DESC
                """ 
    
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            
        except Exception as e:
            msg = 'get_sow_farrowing_list(); error in executing query[] = ' + sql
            msg += '\n'
            msg += str(e)
            msg += '\n\n'
            self.model.logger.append(
                log_level = LOG_FATAL, tag = self.TAG, msg = msg)
            rows = None
        

        result = []
        if rows is not None:
            
            
            for row in rows:
                cur_ins_id               = row[0]
                cur_sow_number          = row[1]
                cur_date_actual         = str(row[2])
                cur_days_since_ins       = row[3]
                    
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
                    'days_ai':          cur_days_since_ins,
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
    
    
    
    