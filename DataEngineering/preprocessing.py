def appy_preprocess(cat_cols, num_cols, data):
    """
    *Purpose*: applies encoding and normalization on the given dataset
    *Input*: cat_cols = categorical columns, num_cols = numerical columns
             data = original dataset
    *Output*: preprocessed dataset
    """
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.pipeline import Pipeline

    df = data.copy()
    # numerical pipeline:
    num_pipeline = Pipeline(steps=[
        ("scale", StandardScaler())
    ])

    # categorical pipeline
    cat_pipeline = Pipeline(steps=[
        ("encode", OneHotEncoder(sparse_output=False, handle_unknown="ignore"))
    ])

    # combine both into single pipeline
    preprocessor = ColumnTransformer(transformers=[
        ("num", num_pipeline, num_cols),
        ("cat", cat_pipeline, cat_cols)
    ], remainder="passthrough"
    )

    # apply preprocessor to dataset
    preprocessed_array = preprocessor.fit_transform(df)
    feature_names = preprocessor.get_feature_names_out()
    
    import pandas as pd
    preprocessed_df = pd.DataFrame(preprocessed_array, columns=feature_names)

    return preprocessed_df