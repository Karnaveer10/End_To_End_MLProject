import os 
import sys

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder 
from sklearn.pipeline import Pipeline
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from sklearn.compose import ColumnTransformer
import numpy as np 
import pandas as pd
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")  

class DataTransformation:
    def __init__(self):
        self.config = DataTransformationConfig()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting Data Transformation phase")
    
    def get_data_transformer_object(self, train_path, test_path):
        try:
            df = pd.read_csv(train_path)
            num_feat = df.select_dtypes(exclude='object').columns
            cat_feat = df.select_dtypes(include='object').columns
            target_column_name = "math_score"
            num_feat = [feat for feat in num_feat if feat != target_column_name]
            self.logger.info(f"Numerical columns: {num_feat}")
            self.logger.info(f"Categorical columns: {cat_feat}")
            
            num_pipeline = Pipeline( 
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )
            
            cat_pipeline = Pipeline(  
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                ]
            )
            
            preprocessor = ColumnTransformer(  
                [ 
                    ("Numerical_transformer", num_pipeline, num_feat),  # ✅ FIXED: "NUmerical" → "Numerical"
                    ("Cat_Transformer", cat_pipeline, cat_feat)
                ]
            )
            return preprocessor
            
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self, train_path, test_path): 
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            preprocessing_obj = self.get_data_transformer_object(train_path, test_path)
            
            target_column_name = "math_score"
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)

            target_feature_train_df = train_df[target_column_name]
            target_feature_test_df = test_df[target_column_name]  
            
            self.logger.info(
                "Applying preprocessing object on training dataframe and testing dataframe."
            )
            
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[  
                input_feature_test_arr, np.array(target_feature_test_df)  # ✅ FIXED: Used test target!
            ]

            self.logger.info(f"Saved preprocessing object.")

            save_object(
                file_path=self.config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.config.preprocessor_obj_file_path,
            )
            
        except Exception as e:
            raise CustomException(e, sys)
