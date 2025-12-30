"""
DataIngestion Component - ML Pipeline Step 1
Purpose: Load raw data → Split → Save train/test/raw CSV files
Run from PROJECT ROOT after pip install -e .
"""

import sys
import os
from src.logger import logging  
from src.exception import CustomException  
import pandas as pd
from sklearn.model_selection import train_test_split 
from dataclasses import dataclass  #  Data class (immutable config)
from src.components.data_transformation import DataTransformationConfig
from src.components.data_transformation import DataTransformation
@dataclass  #  @dataclass = auto __init__, no boilerplate
class DataIngestionConfig:
    
    train_data_path: str = os.path.join('artifacts', "train.csv")    
    test_data_path: str = os.path.join('artifacts', "test.csv")      
    raw_data_path: str = os.path.join('artifacts', "data.csv")       

class DataIngestion:
    def __init__(self):  # (instance method)
        """Initialize config + logger for this instance"""
        self.ingestion_config = DataIngestionConfig()  # Config object
        self.logger = logging.getLogger(__name__) 
        '''# Logger for THIS module
        __name__ = "src.components.data_ingestion"
       
        self.logger = "data_ingestion" logger (traceable!)
        '''
    def initiate_data_ingestion(self) -> tuple:  #  -> tuple = return type hint
        """Main method: Load → Split → Save → Return paths"""
        self.logger.info("Entered Data ingestion component")  # self.logger
        try:
            df = pd.read_csv('notebook/data/stud.csv') 
            self.logger.info(f"Reading Dataset - Shape: {df.shape}")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            self.logger.info("Train test split initiated")
            
            train_set, test_set = train_test_split(
                df, test_size=0.2, random_state=42 
            )
            
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            
            self.logger.info("Ingestion completed successfully")
            
            #Return paths for NEXT pipeline step
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
        except Exception as e:
            self.logger.error(f"Data ingestion failed: {e}")  #  Log error
            raise CustomException(e, sys) # ✅ CustomException(e, sys) syntax

if __name__ == "__main__":  # ✅ Run only if direct execution (not import)
    """Entry point - creates DataIngestion instance + runs pipeline"""
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    print(f"Train saved: {train_data}")
    print(f"Test saved:  {test_data}")
    print("Check artifacts/ folder!")
    
    obj2 = DataTransformation()
    train_arr,test_arr,_=obj2.initiate_data_transformation(train_data,test_data)



'''
ALL THESE FUNCTIONS ARE ALREADY PRESENT IN DATACLASS ..LESS BOILERPLATE

print(config)  # AUTO __repr__: DataIngestionConfig(train_data_path='train.csv')
config2 = DataIngestionConfig()
print(config == config2)  # AUTO __eq__: True
'''