"""
Creates timestamped log files 

FILE STRUCTURE:
ML_Project/
├── logs/
│   └── 12_30_2025_04_29_15.log  ← Auto-created!
├── src/
│   └── logger.py
"""
import logging 
import os    
from datetime import datetime  


# ========== DYNAMIC TIMESTAMPED LOG FILE ==========
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


# ========== BUG FIX: Create logs FOLDER (not nested) ==========
log_dir = os.path.join(os.getcwd(), "logs")  # /project/logs/
os.makedirs(log_dir, exist_ok=True)          # Create if missing

# FIXED LOG PATH: logs/12_30_2025_04_29_15.log
LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)


# ========== PROFESSIONAL LOGGING CONFIGURATION ==========
logging.basicConfig(
    # WRITE TO FILE (not console)
    filename=LOG_FILE_PATH,
    
    # CUSTOM FORMAT: [TIMESTAMP] LINE MODULE - LEVEL - MESSAGE
    # CUSTOM FORMAT: [TIMESTAMP] LINE MODULE - LEVEL - MESSAGE
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    # 
    # %(asctime)s   = "2025-12-30 04:29:15,123"
    # %(lineno)d    = 45 (EXACT line number)
    # %(name)s      = "src.train" (module name)
    # %(levelname)s = "INFO" / "ERROR" / "WARNING"
    # %(message)s   = "Training started"
    
    # SAMPLE OUTPUT:
    # [2025-12-30 04:29:15] 45 src.train - INFO - Training started
    # [2025-12-30 04:29:20] 67 src.train - ERROR - Model failed
    # 
    
    # MINIMUM LEVEL: INFO and above (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    level=logging.INFO
)




"""
========== USAGE IN YOUR ML FILES ==========

# src/train.py
from src.logger import logging  # ← Import configured logger
logger = logging.getLogger(__name__)  # ← Get logger for this module

logger.info("🚀 Starting ML training...")
logger.warning("⚠️ Low data quality detected")
logger.error("💥 Model training failed!")

# Auto-saves to: logs/12_30_2025_04_29_15.log
"""
