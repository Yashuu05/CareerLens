import os 
import sys
import pandas as pd
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from pathlib import Path
from PlacementPrediction.ml_utils import prepare_test_train
from logger import logging as log

DATA_DIRECTORY = r"D:\projects\Student\dataset\processed\preprocessed_data.csv"
TARGET = "remainder__placement_status"

def testSmote():

    # read data
    try:
        log.info(f"loading dataset from {DATA_DIRECTORY}")
        df = pd.read_csv(DATA_DIRECTORY)
        print("dataset load successfully.")
        log.info(f"{DATA_DIRECTORY} load successful.")

    except Exception as e:
        log.error(f"{e}")
        print(f"error while reading dataset: {e}")
        
    _,y_train,_,_ = prepare_test_train(
        data=df,
        target=TARGET,
        randomState=42,
        testSize=0.25,
    )
    
    count_of_0 = len(y_train[y_train == 0])
    count_of_1 = len(y_train[y_train == 1])

    assert int(count_of_1) == int(count_of_0)


if __name__ == "__main__":
    log.info("testing of SMOTE initiated")
    testSmote()
    log.info("Testing End.")