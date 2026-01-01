"""
CUSTOM EXCEPTION HANDLER - src/exception.py
WHY: Basic 'except Exception' loses CRITICAL debugging info.
This gives EXACT file + line number of failures

"Error in train.py line 45: model.fit failed"
"""
import sys
from src.logger import logging 

def error_message_detail(error, error_detail: sys):
    """
    EXTRACTS PRECISE ERROR LOCATION:
    - File name (train.py)
    - Line number (45)
    - Error message (ValueError: invalid shape)
    """
    _, _, exc_tb = error_detail.exc_info()
    
    file_name = exc_tb.tb_frame.f_code.co_filename  
    line_number = exc_tb.tb_lineno        
    
    # FORMATTED ERROR with CONTEXT
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, line_number, str(error)
    )
    
    return error_message


class CustomException(Exception):
    """
    PRODUCTION-READY EXCEPTION:
    - Inherits from Exception (standard)
    - Auto-captures EXACT error location
    """
    def __init__(self, error_message: str, error_detail: sys):
        """
        USAGE:
        raise CustomException("Training failed", sys)
        """
        # Pass original message to parent Exception
        super().__init__(error_message)
        
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
    
    def __str__(self):
        """What gets printed when exception raised"""
        return self.error_message

'''
1. EXCEPTION OCCURS ↓
   model.fit(X, y)  # ← FAILS (line 45)

2. TRY/EXCEPT CATCHES ↓
   except Exception as e:
       raise CustomException("Training failed", sys)  # ← CREATE OBJECT

3. __init__() RUNS AUTOMATICALLY ↓
   def __init__(self, "Training failed", sys):
       super().__init__("Training failed")           # ← Parent Exception setup
       self.error_message = error_message_detail(...) # ← CALLS YOUR FUNCTION

4. error_message_detail() EXECUTES ↓
   def error_message_detail("Training failed", sys):
       sys.exc_info() → "train.py", line 45
       return "Error in [train.py] line [45] message[Training failed]"

5. OBJECT NOW HAS DATA ↓
   CustomException object:
   ├── Exception.message = "Training failed"     (parent)
   └── self.error_message = "Error in train.py line 45"  (custom)

6. RAISE/PRINT → __str__() RUNS ↓
   def __str__(self):
       return self.error_message  # ← "Error in train.py line 45"

'''