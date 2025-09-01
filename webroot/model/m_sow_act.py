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
    
    
    def get_pig_prod_list(self, is_active = 0, is_growing = 0, is_harvested = 0, 
            year = None, sow = None):
        """
        Will get list of pig production list.
        
        Parameters
        ----------
        is_active : int
            if > 0, pig production with status gestating, lactating and weaning 
               will be returned
            
        is_growing : int
            if > 0, pig production with status growing, fattening, finishing will be returned
  
        is_harvested : int
            if > 0, pig production with status harvested will be returned
            
       
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
        order_by        = ' a.sow_id DESC, a.id DESC'
        
        if sow is not None:
            where_clause = "WHERE a.sow_number = '%s'" % sow
            
        else:
            if is_harvested > 0:
                where_clause = 'WHERE status_id = 10 '
                
                if year is not None:
                    where_clause += ' AND YEAR(a.date_weaning) =  %s ' % year
                
                order_by        = 'a.date_weaning DESC '
               
            else:
            
                if is_growing > 0:
                    where_clause = 'WHERE a.status_id IN (5,7,8,9)'
                    if year is not None:
                        where_clause += ' AND YEAR(a.date_weaning) =  %s ' % year
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
                    
                    a.num_pigs_dead_at_birth,
                    a.num_pigs_live_m,
                    a.num_pigs_live_f,
                    a.num_pigs_weaning_m,
                    a.num_pigs_weaning_f,
                    
                    a.date_weaning
         
                FROM pig_production a
                LEFT OUTER JOIN pig_prod_status b           ON a.prod_status_id = b.id
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
                
                cur_date_actual         = str(row[4]) if row[4] else None
                cur_num_days_actual     = row[5] if row[5] else None
                    
                cur_status_id           = row[6]
                cur_semen_desc          = row[7]
                cur_status              = row[8]
                    
                cur_num_b_dead          = row[9] if row[9] else None
                cur_num_b_male          = row[10] if row[10] else None
                cur_num_b_female        = row[11] if row[11] else None
                    
                cur_num_w_male          = row[12] if row[12] else None
                cur_num_w_female        = row[13] if row[13] else None
                
                cur_num_w_dead          = None
                if cur_num_w_male is not None and cur_num_w_female is not None:
                    cur_num_w_dead = cur_num_b_male + cur_num_b_female - \
                                        cur_num_w_male - cur_num_w_female
                                        
                                        
                cur_date_weaning        = str(row[14]) if row[14] else None
                
                
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
    
    
    def get_pig_prod_feeding_list(self, is_growing = 0):
        
        # Check if still connected to database
        if self.model.check_if_connected() == False:
            # Make new connection
            self.model.connect_to_db()

        # Get database connection
        conn = self.model.db_conn
        
        where_clause = 'WHERE a.status_id IN (4, 5,7,8,9)'
        if is_growing > 0:
            where_clause = 'WHERE a.status_id IN (5,7,8,9)'
       
        sql =   """
                SELECT 
                    a.id,
                    b.sow_number,
                    b.name AS sow_name,
                    
                    a.status_id,
                    c.name AS prod_status,
                    
                    a.num_pigs_current_m,
                    a.num_pigs_current_f,
                    
                    a.date_actual_birth,
                    
                    a.date_iron_1,
                    a.date_iron_2,
                    a.date_vitamins_1,
                    a.date_kapon,
                    a.date_vitamins_2,
                    a.date_deworm_1,
                    
                    a.date_booster,
                    a.date_prestarter,
                    a.date_weaning,
                    a.date_starter,
                    a.date_grower,
                    a.date_finisher,
                    
                    a.num_b_lactating,
                    a.num_b_booster,
                    a.num_b_prestarter,
                    a.num_b_starter,
                    a.num_b_grower,
                    a.num_b_finisher,
                    
                    a.num_l_lactating,
                    a.num_l_booster,
                    a.num_l_prestarter,
                    a.num_l_starter,
                    a.num_l_grower,
                    a.num_l_finisher,
                    
                    a.cost_lactating,
                    a.cost_booster,
                    a.cost_prestarter,
                    a.cost_starter,
                    a.cost_grower,
                    a.cost_finisher,
                    
                    a.date_harvest
                    
                FROM pig_production a
                LEFT OUTER JOIN sow b ON a.sow_id = b.id
                LEFT OUTER JOIN pig_prod_status c ON a.prod_status_id = c.id
                %s
                ORDER BY a.date_actual_birth DESC
                """ % where_clause 
    
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()

        except Exception as e:
            msg = 'get_pig_prod_feeding_list(); error in executing query[] = ' + sql
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
                cur_sow_name            = row[2]
                
                cur_status_id           = row[3]
                cur_status_name         = row[4]
                
                cur_num_c_male          = row[5] if row[5] else None
                cur_num_c_female        = row[6] if row[6] else None
               
                cur_date_actual         = str(row[7])
                
                cur_date_iron_1         = str(row[8])  if row[8]  else None
                cur_date_iron_2         = str(row[9])  if row[9]  else None
                cur_date_vitamins_1     = str(row[10]) if row[10] else None
                cur_date_kapon          = str(row[11]) if row[11] else None
                cur_date_vitamins_2     = str(row[12]) if row[12] else None
                cur_date_deworm_1       = str(row[13]) if row[13] else None
                
                
                cur_date_booster        = str(row[14]) if row[14] else None
                cur_date_prestarter     = str(row[15]) if row[15] else None
                cur_date_weaning        = str(row[16]) if row[16] else None
                cur_date_starter        = str(row[17]) if row[17] else None
                cur_date_grower         = str(row[18]) if row[18] else None
                cur_date_finisher       = str(row[19]) if row[19] else None
                
                cur_num_b_lactating     = row[20]
                cur_num_b_booster       = row[21]
                cur_num_b_prestarter    = row[22]
                cur_num_b_starter       = row[23]
                cur_num_b_grower        = row[24]
                cur_num_b_finisher      = row[25]
                
                cur_num_l_lactating     = float(row[26]) if row[26] is not None else None
                cur_num_l_booster       = float(row[27]) if row[27] is not None else None
                cur_num_l_prestarter    = float(row[28]) if row[28] is not None else None
                cur_num_l_starter       = float(row[29]) if row[29] is not None else None
                cur_num_l_grower        = float(row[30]) if row[30] is not None else None
                cur_num_l_finisher      = float(row[31]) if row[31] is not None else None
                
                cur_cost_lactating      = row[32]
                cur_cost_booster        = row[33]
                cur_cost_prestarter     = row[34]
                cur_cost_starter        = row[35]
                cur_cost_grower         = row[36]
                cur_cost_finisher       = row[37]
                
                cur_date_harvest        = row[38]
                
                
                cur_num_c_lactating     = None
                cur_num_c_booster       = None
                cur_num_c_prestarter    = None
                cur_num_c_starter       = None
                cur_num_c_grower        = None
                cur_num_c_finisher      = None
            
            
                if cur_num_b_lactating is not None and cur_num_l_lactating is not None:
                    cur_num_c_lactating = float(cur_num_b_lactating) - cur_num_l_lactating
                
                if cur_num_b_booster is not None and cur_num_l_booster is not None:
                    cur_num_c_booster = float(cur_num_b_booster) - cur_num_l_booster
                
                if cur_num_b_prestarter is not None and cur_num_l_prestarter is not None:
                    cur_num_c_prestarter = float(cur_num_b_prestarter) - cur_num_l_prestarter
                
                if cur_num_b_starter is not None and cur_num_l_starter is not None:
                    cur_num_c_starter = float(cur_num_b_starter) - cur_num_l_starter
                
                if cur_num_b_grower is not None and cur_num_l_grower is not None:
                    cur_num_c_grower = float(cur_num_b_grower) - cur_num_l_grower
                
                if cur_num_b_finisher is not None and cur_num_l_finisher is not None:
                    cur_num_c_finisher = float(cur_num_b_finisher) - cur_num_l_finisher
                
                
                cur_entry = {
                    'id':               cur_id,
                    
                    'sow': {
                        'number':       cur_sow_number,
                        'name':         cur_sow_name,
                    },
                    
                    'status_id':        cur_status_id, 
                    'status':           cur_status_name,
                    
                    'num_pigs_current': {
                        'male':         cur_num_c_male,
                        'female':       cur_num_c_female
                    },
                    
                    'dates':{
                        'birth':        cur_date_actual,
                        
                        'iron_1':       cur_date_iron_1,
                        'iron_2':       cur_date_iron_2,
                        'vitamins_1':   cur_date_vitamins_1,
                        'kapon':        cur_date_kapon,
                        'vitamins_2':   cur_date_vitamins_2,
                        'deworm_1':     cur_date_deworm_1,
                        
                        'booster':      cur_date_booster,
                        'prestarter':   cur_date_prestarter,
                        'weaning':      cur_date_weaning,
                        'starter':      cur_date_starter,
                        'grower':       cur_date_grower,
                        'finisher':     cur_date_finisher
                    },
                    
                    'num_feeds': {
                        'lactating': {
                            'bought':   cur_num_b_lactating,
                            'consumed': cur_num_c_lactating,
                            'left':     cur_num_l_lactating
                        },
                        
                        'booster': {
                            'bought':   cur_num_b_booster,
                            'consumed': cur_num_c_booster,
                            'left':     cur_num_l_booster
                        },
                            
                        'prestarter': {
                            'bought':   cur_num_b_prestarter,
                            'consumed': cur_num_c_prestarter,
                            'left':     cur_num_l_prestarter
                        },
                            
                        'starter': {     
                            'bought':   cur_num_b_starter,
                            'consumed': cur_num_c_starter,
                            'left':     cur_num_l_starter
                        },
                        
                        'grower': {
                            'bought':   cur_num_b_grower,
                            'consumed': cur_num_c_grower,
                            'left':     cur_num_l_grower
                        },
                        
                        'finisher': {    
                            'bought':   cur_num_b_finisher,
                            'consumed': cur_num_c_finisher,
                            'left':     cur_num_l_finisher
                        }
                    },
                    
                    'cost_feeds': {
                        'lactating':    cur_cost_lactating,
                        'booster':      cur_cost_booster,
                        'prestarter':   cur_cost_prestarter,
                        'starter':      cur_cost_starter,
                        'grower':       cur_cost_grower,
                        'finisher':     cur_cost_finisher
                    }
                   
                }
                result.append(cur_entry)

        
        return result
        
    
    
    def get_sow_operations_list(self):
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
                    a.sow_number,
                    a.sow_status_id,
                    b.name AS status,
                    a.last_prod_id, 
                    
                    c.date_insemination
                    
                FROM sow a
                LEFT OUTER JOIN sow_status      b  ON a.sow_status_id = b.id
                LEFT OUTER JOIN pig_production  c  ON a.last_prod_id = c.id
                WHERE a.date_culled IS NULL
                ORDER BY c.date_insemination
                """ 
    
        rows = None
        
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            
            rows = cursor.fetchall()
            cursor.close()
            #conn.close()
            
        except Exception as e:
            msg = 'get_sow_operations_list(); error in executing query[] = ' + sql
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
                cur_status_id           = row[1]
                cur_status_name         = row[2]
                cur_last_prod_id        = row[3]
                cur_last_date_insem     = str(row[4]) if row[4] else None
                
                cur_entry = {
                    'sow_number':       cur_sow_number, 
                    'status_id':        cur_status_id,
                    'status_name':      cur_status_name,
                    'last_prod_id':     cur_last_prod_id,
                    'date_insemination': cur_last_date_insem
                }
                
                result.append(cur_entry)

        
        return result
    
    
    
    