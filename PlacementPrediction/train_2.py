import os 
import sys
import yaml
import optuna
import mlflow
import ensure
import pandas as pd
import joblib
from pathlib import Path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from logger import logging as log
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from PlacementPrediction.ml_utils import *

DATA_DIRECTORY = r"D:\projects\Student\dataset\processed\preprocessed_data.csv"
HYPERPARAMETER_PATH = r"D:\projects\Student\PlacementPrediction\hyperparamters.yaml"

@ensure
def read_yaml(file_path: Path) -> dict:
    """
    *Purpose*: read the yaml file (specifically hyperparameters)
    *Input*: 
    - file_path: insert path of yaml file
    *Output*:
    - data: yaml file in dictionary format
    """
    with open(f"{file_path}", "r") as file:
        try:
            data = yaml.safe_load(file)
            return data

        except yaml.YAMLError as error:
            log.error(f"{error}")
            print(f"Error parsing YAML: {error}")
            return None
    
def train_with_hyperparameters(model, model_name: str, hyperparameter: dict, X_train, y_train, X_test, y_test, trial: int):
    """
    *Purpose* : training several machine learning algorithm by using hyperparameters
    *inputs*: 
    1. model = machine learning algorithm class
    2. model_name = name of the model ('random_forest' or 'logistic_regression')
    3. hyperparameter = dictionary of hyperparameters
    4. X_train = input training data
    5. y_train = input actual target value
    6. X_test = input test data
    7. y_test = input test target value
    8. trial = number of optuna trials

    *output*:
    - performance results
    """
    def objective(optuna_trial):
        with mlflow.start_run(nested=True):
            # Define the hyperparameter search space using the 'optuna_trial' object
            params = {}
            if model_name == "random_forest":
                params["n_estimators"] = optuna_trial.suggest_categorical("n_estimators", hyperparameter["random_forest"]["n_estimators"])
                params["max_depth"] = optuna_trial.suggest_categorical("max_depth", hyperparameter["random_forest"]["max_depth"])
                params["min_samples_split"] = optuna_trial.suggest_categorical("min_samples_split", hyperparameter["random_forest"]["min_samples_split"])
                params["min_samples_leaf"] = optuna_trial.suggest_categorical("min_samples_leaf", hyperparameter["random_forest"]["min_samples_leaf"])
                params["criterion"] = hyperparameter["random_forest"]["criterion"]
                params["n_jobs"] = hyperparameter["random_forest"]["n_jobs"]
                params["random_state"] = hyperparameter["random_forest"]["random_state"]
            elif model_name == "logistic_regression":
                params["solver"] = optuna_trial.suggest_categorical("solver", hyperparameter["logistic_regression"]["solver"])
                params["penalty"] = optuna_trial.suggest_categorical("penalty", hyperparameter["logistic_regression"]["penalty"])
                params["C"] = optuna_trial.suggest_categorical("C", hyperparameter["logistic_regression"]["C"])
                params["max_iter"] = optuna_trial.suggest_categorical("max_iter", hyperparameter["logistic_regression"]["max_iter"])
                params["class_weight"] = hyperparameter["logistic_regression"]["class_weight"][0]
                params["random_state"] = hyperparameter["logistic_regression"]["random_state"]
                
                # handle invalid combinations for LogisticRegression
                if params["penalty"] == "l1" and params["solver"] not in ["liblinear", "saga"]:
                    raise optuna.exceptions.TrialPruned()

            # initialize model with params
            clf = model(**params)

            # create pipeline
            model_pipeline = create_model_pipeline(model=clf, n_components=0.95)
            # fit model
            model_pipeline.fit(X_train, y_train)
            # evaluate model
            performance = evaluate_model(model=model_pipeline, X_test=X_test, y_test=y_test)
            accuracy = performance[0]

            # log to mlflow
            mlflow.log_params(params)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("recall", performance[1])
            mlflow.log_metric("precision", performance[2])
            mlflow.log_metric("f1_score", performance[3])
            mlflow.log_metric("roc_auc", performance[4])
            
            return accuracy

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=trial)

    print(f"Best trial for {model_name}: {study.best_trial.value}")
    print(f"Best params for {model_name}: {study.best_trial.params}")
    
    # Re-train with best parameters
    best_params = study.best_trial.params
    final_params = {}
    if model_name == "random_forest":
        final_params["n_estimators"] = best_params["n_estimators"]
        final_params["max_depth"] = best_params["max_depth"]
        final_params["min_samples_split"] = best_params["min_samples_split"]
        final_params["min_samples_leaf"] = best_params["min_samples_leaf"]
        final_params["criterion"] = hyperparameter["random_forest"]["criterion"]
        final_params["n_jobs"] = hyperparameter["random_forest"]["n_jobs"]
        final_params["random_state"] = hyperparameter["random_forest"]["random_state"]
    elif model_name == "logistic_regression":
        final_params["solver"] = best_params["solver"]
        final_params["penalty"] = best_params["penalty"]
        final_params["C"] = best_params["C"]
        final_params["max_iter"] = best_params["max_iter"]
        final_params["class_weight"] = hyperparameter["logistic_regression"]["class_weight"][0]
        final_params["random_state"] = hyperparameter["logistic_regression"]["random_state"]
        
    best_clf = model(**final_params)
    best_pipeline = create_model_pipeline(model=best_clf, n_components=0.95)
    log.info(f"Retraining {model_name} with best parameters.")
    print(f"Retraining {model_name} with best parameters...")
    # retrain model
    best_pipeline.fit(X_train, y_train)
    
    log.info("evaluation of best model")
    print("evaluating best model...")
    performance = evaluate_model(model=best_pipeline, X_test=X_test, y_test=y_test)
    log.info(f"Retraining of {model_name} completed.")

    print(f"saving {model_name}...")
    # Save best model
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, f"{model_name}.joblib")
    joblib.dump(best_pipeline, model_path)
    print(f"Best model saved at {model_path}")

    return study.best_trial, final_params, performance

###########################################################################################
if __name__ == "__main__":
    print("========== training initiated =========")
    log.info("Initiated training pipeline")
    mlflow.set_experiment(experiment_name="training 2")
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
    log.info("Dataset split and SMOTE completed.")

    log.info("Reading YAML file")
    # load hyperparameters file
    hyperparams_file = read_yaml(file_path=HYPERPARAMETER_PATH)
    print("Hyperparameter file load successful")
    # define model
    ml_model = RandomForestClassifier
    # train ml algorithms
    log.info("Initiating training")
    mlflow.sklearn.autolog()
    _,best_params, results = train_with_hyperparameters(
        model= ml_model,
        model_name="random_forest",
        hyperparameter=hyperparams_file,
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        trial=10
    )

    print(f"\n Best Parameters: \n", best_params)
    print(f"\nPerformance results: \n", results)

    log.info("Training Terminated")
    print("======= End ========")
