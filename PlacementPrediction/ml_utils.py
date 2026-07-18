def prepare_test_train(data,target="remainder__placement_status",randomState=0, testSize=0.20):
    """
    *Purpose*: 
    - To split dataset into train and test
    - Apply SMOTE to handle imbalanced values

    *input*:
    - data: processed dataset in .csv format
    - target: target feature
    - random_state: int (default: 0)
    - test_size: float (default: 0.20)
    
    *outputs*:
    - X_train_smote = applied SMOTE on X_train
    - y_train_smote = applied SMOTE on y_train
    - X_test = input test dataset
    - y_test = output test values
    """
    from sklearn.model_selection import train_test_split
    from imblearn.over_sampling import SMOTE
    df = data.copy()
    y = df[target]
    X = df.drop(target, axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=randomState, test_size=testSize, shuffle=True)
    # apply SMOTE
    smote = SMOTE(sampling_strategy='minority', random_state=randomState)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

    return X_train_smote, y_train_smote, X_test, y_test

def create_model_pipeline(model, n_components=0.95):
    """
    *Purpose*: create Pipeline and applies PCA
    
    *inputs*:
    - model: model object
    - n_components: PCA 

    *output*:
    1. model_pipeline: PCA and model pipeline
    """

    from sklearn.pipeline import Pipeline
    from sklearn.decomposition import PCA

    model_pipeline = Pipeline(steps=[
        ('pca', PCA(n_components=n_components)),
        ("model", model)
    ])

    return model_pipeline

# evaluation of model
def evaluate_model(model, X_test, y_test) -> list:
    """
    *purpose* : to evaluate performance of model 

    *inputs*:
    - model: fitted model 
    - X_test: input test dataset
    - y_test: input target value

    *output*:
    - peformance_lst = list of performance metrics
    """
    
    from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, roc_auc_score
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_pred)

    performance_lst = [accuracy, recall, precision, f1, roc]
    return performance_lst