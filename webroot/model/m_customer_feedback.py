# March 12, 2026
# Jack Wong
import os
import sys

from common_constants       import *

# Include the directory where this file is located 
module_file_path            = os.path.abspath(__file__)
module_directory            = os.path.dirname(module_file_path)

if module_directory not in sys.path:
   sys.path.append(module_directory)

from base_model             import BaseModel



class CustomerFeedback(BaseModel):
    def __init__(self, model):
        super().__init__(model)


    def add(self, data = None):
        """
        PROCEDURE customer_feedback_add(
            in_user_id              INT,
           
            in_notes                VARCHAR(500)
        )  
        """
        
        params = [
            data.user_id,
            data.notes              if data.notes and data.notes.strip() else None
        ]
        
        res = self._call_procedure('customer_feedback_add', params)
        
        if res is None:
            return None
        
        
        row = res[0]
        

        if row is not None:
            return {
                'result':{
                    'num':              row[0],
                    'code':             row[1],
                    'desc':             row[2],
                },
                
                'customer_feedback': {
                    'id':               row[3]
                }
            }

        return None
    
    
