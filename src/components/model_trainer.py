import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import os 
import sys
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")
    
class Model_Trainer:
    def __init__ (self):
        self.logger = logging.getLogger(__name__)
        self.config = ModelTrainerConfig()
    def initiate_model_trainer(self,train_array,test_array):
        try:
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }
            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                # "Gradient Boosting":{
                #     # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                #     'learning_rate':[.1,.01,.05,.001],
                #     'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                #     # 'criterion':['squared_error', 'friedman_mse'],
                #     # 'max_features':['auto','sqrt','log2'],
                #     'n_estimators': [8,16,32,64,128,256]
                # },
                "Linear Regression":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                # "CatBoosting Regressor":{
                #     'depth': [6,8,10],
                #     'learning_rate': [0.01, 0.05, 0.1],
                #     'iterations': [30, 50, 100]
                # },
                # "AdaBoost Regressor":{
                #     'learning_rate':[.1,.01,0.5,.001],
                #     # 'loss':['linear','square','exponential'],
                #     'n_estimators': [8,16,32,64,128,256]
                # }
                
            }
            self.logger.info("SPlitting train and test for model training")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            self.logger.info("Starting Model Training")

            model_report = evaluate_models(
    X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test,
    models=models, params=params 
)

            print(" Model Report:", model_report)

            sorted_report = dict(sorted(model_report.items(), 
                                    key=lambda x: x[1][0], reverse=True))

            best_model_object = list(sorted_report.items())[0]
            best_model_name = best_model_object[0]
            best_model_score = best_model_object[1][0]
            best_params = best_model_object[1][1]

            best_model = models[best_model_name].set_params(**best_params)
            best_model.fit(X_train, y_train) 

            if best_model_score < 0.7:
                raise CustomException("No acceptable model found (R² < 0.7)", sys.exc_info())

            self.logger.info(f" Best model found: {best_model_name} (CV R²: {best_model_score:.3f})")

            save_object(
                file_path=self.config.trained_model_file_path,
                obj=best_model 
            )

            # Test final performance
            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)

            self.logger.info(f"Final test R²: {r2_square:.3f}")
            return r2_square

        except Exception as e:
            raise CustomException(e,sys)
