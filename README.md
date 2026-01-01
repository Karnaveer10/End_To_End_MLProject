#  End-to-End Machine Learning Project: Student Performance Predictor

A **clean, professional, and modular** Machine Learning application built using industry-standard practices. This project demonstrates the transition from a notebook-based experiment to a **production-ready web application**.

>  **Important Note** > The **dataset and modeling techniques are intentionally not complex**. The **primary goal** of this project is to showcase **clean architecture, modular code structure, robust pipelines, and deployment best practices**.

---

##  Project Overview

This project builds a **modular ML pipeline in Python** and exposes it via a **FastAPI web application**, where users can submit student details through a form and receive a **predicted math score**.

###  Main Objectives
- Demonstrate how to structure a **real multi-module ML codebase** instead of a single notebook.
- Implement **robust preprocessing, model evaluation, logging, and exception handling**.
- Showcase **deployment of an ML model to the cloud (Render)** with an HTML-based UI.

###  Live Deployment
- **Prediction Endpoint:** [https://mlproject-6mdv.onrender.com/predictdata](https://mlproject-6mdv.onrender.com/predictdata)

---

## Tech Stack

| Layer | Tools |
| :--- | :--- |
| **Language** | Python 3.x |
| **Data / ML** | Pandas, NumPy, Scikit-learn, XGBoost, CatBoost |
| **Backend API** | FastAPI, Jinja2 |
| **Frontend UI** | HTML Templates |
| **Deployment** | Render |
| **Utilities** | Custom Logging, Custom Exceptions, Artifact Serialization |

---

##  Dataset

The dataset used is a **public Kaggle student performance dataset**, chosen so that the focus remains on **system design**.

* **Kaggle Dataset:** [Student Performance in Exams](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams)

---

##  Project Structure

```text
End_To_End_MLProject/
├── app.py                      # FastAPI app (routes + templates)
├── src/
│   ├── components/
│   │   ├── data_ingestion.py       # Reads raw data, train/test split
│   │   ├── data_transformation.py  # Preprocessing pipelines
│   │   └── model_trainer.py        # Model training & selection
│   ├── pipeline/
│   │   └── predict_pipeline.py     # Prediction pipeline used by API
│   ├── exception.py                # Custom exception handling
│   ├── logger.py                   # Central logging configuration
│   └── utils.py                    # Utility helpers (save/load objects)
├── templates/
│   ├── index.html                  # Landing page
│   └── home.html                   # Prediction form + results
├── artifacts/                  # Models, preprocessors, data splits
├── requirements.txt
└── README.md
```
## End-to-End ML Pipeline

### 1. Data Ingestion

- Loads raw student performance data from CSV  
- Performs train-test split  
- Saves processed datasets into the `artifacts/` directory  

---

### 2. Data Transformation

- Automatically identifies numerical and categorical columns  
- Builds preprocessing pipelines:

#### Numerical Features
- Median imputation  
- Standard scaling  

#### Categorical Features
- Most-frequent imputation  
- One-hot encoding  

- Combines pipelines using `ColumnTransformer`  
- Fits the preprocessor on training data  
- Saves the fitted preprocessor to:
  ```text
  artifacts/preprocessor.pkl
    ```

## 3. Model Training

### Candidate regression models include:
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor
- XGBoost Regressor
- CatBoost Regressor
- AdaBoost Regressor

### For each model:
- Runs GridSearchCV with model-specific hyperparameter grids
- Evaluates cross-validated R² scores
- Stores results in a performance report

### Best Model Selection

- Chooses the model with the highest performance

- Retrains it on the full training data

- Saves the trained model to:
```text
 artifacts/model.pkl
```

- An optional minimum R² threshold can be enforced

- If unmet, a CustomException is raised

### Prediction Pipeline

#### CustomData
- Converts raw user inputs from the UI into a Pandas DataFrame with the correct schema

#### PredictPipeline
- Loads the saved preprocessor and trained model
- Applies identical transformations used during training
- Generates the predicted math score

## FastAPI Web Application

- Built using FastAPI

- Uses Jinja2 templates for HTML rendering

### Provides:

 - Landing page

 - Interactive prediction form

 - Real-time inference results

## Getting Started (Local Setup)

### 1 Clone the Repository

```
git clone https://github.com/Karnaveer10/End_To_End_MLProject.git
cd End_To_End_MLProject
```

### 2️ Create and Activate Virtual Environment

```
python -m venv venv
 Windows
venv\Scripts\activate

 Linux / macOS
source venv/bin/activate
```

### 3️ Install Dependencies
```
pip install -r requirements.txt
```

### 4️ Run ML Pipeline (Recommended Once)


#### Data ingestion
```
python -m src.components.data_ingestion
```
#### Data transformation
```
python -m src.components.data_transformation
```
#### Model training
```
python -m src.components.model_trainer
```

### 5️ Run the FastAPI App
```
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Access locally:
```
http://localhost:8000/

http://localhost:8000/predictdata
```

## Logging & Error Handling

### Logging

- Centralized logging configured in src/logger.py
- Logs are written to the logs/ directory

### Custom Exception Handling

- Implemented via CustomException in src/exception.py

- Makes debugging ingestion, transformation, and training failures easier
