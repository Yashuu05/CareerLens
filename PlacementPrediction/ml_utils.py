def prepare_test_train(data,target="remainder__placement_status",randomState=0, testSize=0.20):
    """
    *Purpose*: 
    - To split dataset into train and test
    - Apply SMOTE to handle imbalanced values

    *input*:
    - data: processed dataset
    
    *outputs*:
    - X_train_smote = applied SMOTE on X_train
    - y_train_smote = applied SMOTE on y_train
    - X_test = input test dataset
    - y_test = output test values
    """
    from sklearn.model_selection import train_test_split
    from imblearn.over_sampling import SMOTE
    df = data.copy()
    y = df["remainder__placement_status"]
    X = df.drop("remainder__placement_status", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=randomState, test_size=testSize, shuffle=True)
    # apply SMOTE
    smote = SMOTE(sampling_strategy='minority', random_state=randomState)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

    return X_train_smote, y_train_smote, X_test, y_test