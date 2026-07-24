import os 
import sys
from pathlib import Path
import joblib
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not project_root in sys.path:
    sys.path.insert(project_root,0)
from DataEngineering import feature_extraction, preprocessing

MODEL_DIR = "D:\projects\Student\PlacementPrediction\models\logistic_regression.joblib"

def load_model(file_path: Path):
    try:
        model = joblib.load(filename=file_path)
        return model
    except Exception as e:
        return None

def predict_placement(model, input_data: dict):
    """
    *purpose*: To predict the if placement or not 
    *inputs*:
    1. model: trained model
    2. input_data: data input for prediction
    *outputs*:
    1. result: "placed" or not "placed"
    2. probability : probability of prediected output
    """
    import pandas as pd
    input = pd.DataFrame([input_data])
    
    # extract number from college_tier
    if "college_tier" in input.columns:
        input["tier"] = input["college_tier"].str.split("-").str[1].astype("int")
        input = input.drop(["college_tier"], axis=1)

    result = ""
    # apply feature extraction on input data
    new_input = feature_extraction.apply_feature_extraction(data=input)
    num_cols = list(new_input.select_dtypes(exclude="object").columns)
    cat_cols = list(new_input.select_dtypes(include="object").columns)
    
    # remove binary/passthrough features from numerical_cols list for scaling
    if "academic_risk" in num_cols:
        num_cols.remove("academic_risk")

    # preprocess input using StandardScaler and OneHotEncoding
    preprocessed_input = preprocessing.appy_preprocess(cat_cols=cat_cols, num_cols=num_cols, data=new_input)
    
    # Ensure features exactly match what model saw during training
    expected_features = getattr(model, 'feature_names_in_', None)
    if expected_features is not None:
        for col in expected_features:
            if col not in preprocessed_input.columns:
                preprocessed_input[col] = 0
        preprocessed_input = preprocessed_input[expected_features]

    # extract only binary output
    output = model.predict(preprocessed_input)[0]
    if int(output) == 1:
        result = "placed"
    else:
        result = "not placed"
    # probability for output
    probability = max(model.predict_proba(preprocessed_input)[0])

    return result, float(probability)
