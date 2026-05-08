# January 3, 2025
# Jack Wong

from common_constants       import *

class BaseModel:
    def __init__(self, model):
        self.model      = model
        self.TAG        = self.__class__.__name__
    
    
    def _call_procedure(self, proc_name, params):
        """
        Generic stored procedure caller with parameterized queries
        Works for ALL stored procedures across all models
        
        This will always returns an array.
        
        """
        # Build parameterized SQL
        placeholders = ','.join(['%s'] * len(params))
        sql = f"CALL {proc_name}({placeholders})"
        
        
        # Ensure connection
        if not self.model.check_if_connected():
            self.model.connect_to_db()
        
        conn = self.model.db_conn
        
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                
                # Fetch all rows from the result set
                rows = cursor.fetchall()
                return rows
        
        
        except Exception as e:
            proc_call = self._generate_debug_procedure(proc_name, params)
            
            # Send error email to devs
            if self.model.controller is not None:
                subject = 'PigOps: Error procedure call'
                body    = 'Error at: %s\n' % self.TAG
                body    += 'Proc Call: %s\n' % proc_call
                body    += 'Error: %s' % str(e)
                
                self.model.controller.send_email_to_devs(subject, body)
            
            # Log error
            self.model.logger.append(
                log_level=LOG_FATAL,
                tag=self.TAG,
                msg=f"Procedure {proc_name} failed!\n{proc_call}\nError: {e}\n"
            )
        
        return None
    

    def _generate_debug_procedure(self, proc_name, params):
        """
        Generate copy-pasteable SQL string for debugging stored procedures
        ONLY called when procedure fails
        """
        formatted_params = []
        for p in params:
            if p is None:
                formatted_params.append('NULL')
            elif isinstance(p, str):
                # Escape single quotes
                escaped = p.replace("'", "''")
                formatted_params.append(f"'{escaped}'")
            elif isinstance(p, (int, float)):
                formatted_params.append(str(p))
            elif isinstance(p, bool):
                formatted_params.append('1' if p else '0')
            else:
                formatted_params.append(f"'{str(p)}'")
        
        return f"CALL {proc_name}({', '.join(formatted_params)});"
    
    
    def _execute_query(self, sql, params=None):
        """
        Generic SELECT query executor
        Returns rows as list of tuples
        """
        """
        if params is None:
            params = []
        """
        
        if not self.model.check_if_connected():
            self.model.connect_to_db()
        
        conn = self.model.db_conn
        
        try:
            with conn.cursor() as cursor:
                if params:
                    # Parametrized query
                    cursor.execute(sql, params)
                else:
                    # Plain string query
                    cursor.execute(sql)
                
                rows = cursor.fetchall()
                return rows
                
        except Exception as e:
            # Generate debug SQL for troubleshooting
            if params:
                debug_sql = self._generate_debug_query(sql, params)
            else:
                debug_sql = sql
                
                
            # Send error email to devs
            if self.model.controller is not None:
                subject = 'PigOps: Error query'
                body    = 'Error at: %s\n' % self.TAG
                body    += 'SQL: \n'
                body    += debug_sql
                body    += '\nError: %s' % str(e)
                
                self.model.controller.send_email_to_devs(subject, body)
            
            
            self.model.logger.append(
                log_level=LOG_FATAL,
                tag=self.TAG,
                msg=f"Query failed!\n{debug_sql}\nError: {e}\n"
            )
            return None
    
    
    def _generate_debug_query(self, sql, params):
        """
        Generate copy-pasteable SQL string for debugging SELECT queries
        ONLY called when query fails
        """
        if not params:
            return sql + ";"
        
        # Replace %s placeholders with actual values
        debug_sql = sql
        for p in params:
            if p is None:
                debug_sql = debug_sql.replace('%s', 'NULL', 1)
            elif isinstance(p, str):
                # Escape single quotes
                escaped = p.replace("'", "''")
                debug_sql = debug_sql.replace('%s', f"'{escaped}'", 1)
            elif isinstance(p, (int, float)):
                debug_sql = debug_sql.replace('%s', str(p), 1)
            elif isinstance(p, bool):
                debug_sql = debug_sql.replace('%s', '1' if p else '0', 1)
            else:
                debug_sql = debug_sql.replace('%s', f"'{str(p)}'", 1)
        
        return debug_sql + ";"
