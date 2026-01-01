import os
import sys

import numpy as np 
import pandas as pd
import dill
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, params):
    try:
        report = {}
        
        for model_name in models.keys():
            model = models[model_name]
            
            if model_name in params and params[model_name]:
                para = params[model_name]
                gs = GridSearchCV(model, para, cv=3)
                gs.fit(X_train, y_train)
                report[model_name] = (gs.best_score_, gs.best_params_)
            else:
                
                model.fit(X_train, y_train)
                y_test_pred = model.predict(X_test)
                test_r2 = r2_score(y_test, y_test_pred)
                report[model_name] = (test_r2, {})
        
        return report
        
    except Exception as e:
        raise CustomException(e, sys.exc_info()) 
