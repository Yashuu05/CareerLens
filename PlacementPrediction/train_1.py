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
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from PlacementPrediction.ml_utils import *
from logger import logging as log

# dataset path
DATA_DIRECTORY = r"D:\projects\Student\dataset\processed\preprocessed_data.csv"

# models
models = {
    "logistic_regression": LogisticRegression(),
    "decision_tree" : DecisionTreeClassifier(),
    "random_forest" : RandomForestClassifier(n_jobs=-1, random_state=42),
    "lighgbm" : LGBMClassifier(n_jobs=-1, random_state=42),
    "xgboost" : XGBClassifier()
}
# results 
results = {}

# main function to train model
def train_model(models, X_train, y_train, X_test, y_test):
    """
    *Purpose* : training several machine learning algorithm
    *inputs*: 
    1. models = dictionary of several algorithms
    2. X_train = input training data
    3. y_train = input actual target value
    4. X_test = input test data
    5. y_test = input test target value

    *output*:
    - performance results
    """
    for name, model in models.items():
        log.info(f"Initiated training of {name}")
        print(f"training {name}")
        
        # create pipeline
        model_pipeline = create_model_pipeline(model=model, n_components=0.95)
        # fit model
        model_pipeline.fit(X_train, y_train)
        # evaluate model
        performance = evaluate_model(model=model_pipeline, X_test=X_test, y_test=y_test)
        # store in results dict
        results[name] = performance 

    return results

if __name__ == "__main__":
    print("========== training initiated =========")
    log.info("Iniated training pipeline")

    # 1. read preprocessed data
    try:
        log.info(f"Reading dataset from {DATA_DIRECTORY}")
        df = pd.read_csv(DATA_DIRECTORY)
        log.info(f"sucessful dataset load from {DATA_DIRECTORY}")
        print("Dataset load successful")
    except Exception as e:
        print(f"Error: {e}")
        log.error(f"{e}")
    
    # split dataset and use SMOTE
    log.info("splitting dataset and applying smote.")
    X_train, y_train, X_test, y_test = prepare_test_train(
        data=df,
        target="remainder__placement_status",
        randomState=42,
        testSize=0.25,
    )
    print("Training and testing dataset are ready.")

    log.info("initiated ML training.")
    # train ml algorithms
    mlflow.sklearn.autolog()
    result = train_model(models=models, 
                        X_train=X_train, 
                        y_train=y_train, 
                        X_test=X_test, 
                        y_test=y_test
            )
    
    result_df = pd.DataFrame.from_dict(result, orient='index', columns=["accuracy","recall","precision","f1_score","roc_auc"])
    print("saving results...")
    result_df.to_csv(path_or_buf=r"D:\projects\Student\PlacementPrediction\results\performance.csv", index_label="model")
    log.info("results saved in results/ directory.")
    log.info("Training terminated.")
    print(f"========= Training End ===========")