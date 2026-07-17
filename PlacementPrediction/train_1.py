# training models without hyperparameters to select best among them

# 1. create a model pipeline for several algorithms with PCA and no hyperparameters
# 2. split dataset into tain and test
# 3. Use SMOTE to handle imbalanced data
# 4. run the training pipeline
# 5. evaluate each model
# 6. select best model on the basis of f1_sore
import pandas as pd
import mlflow 
import os
import sys 
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from logger import logging as log

# dataset path
DATA_DIRECTIRY = r"D:\projects\Student\dataset\processed\preprocessed_data.csv"

# main function to train model
def train_model():
    """
    *Purpose* : training several machin learning algorithm and selecting best one.
    *inputs*: 
    1. models = dictionary of sevetal algorithms
    2. X_train = input training data
    3. y_train = input actual target value
    4. X_test = input test data
    5. y_test = input test target value

    *output*:
    - performance results
    - best model on the basis of f1_score
    """

if __name__ == "__main__":
    print("========== training initiated =========")
    log.info("Iniated training pipeline")

    # 1. read preprocessed data
    try:
        log.info(f"Reading dataset from {DATA_DIRECTIRY}")
        df = pd.read_csv(DATA_DIRECTIRY)
        log.info(f"sucessful dataset load from {DATA_DIRECTIRY}")
        print("Dataset load successful")
    except Exception as e:
        print(f"Error: {e}")
        log.error(f"{e}")
    
    # split dataset and use SMOTE
