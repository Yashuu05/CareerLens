import pandas as pd
from sklearn.impute import SimpleImputer
from DataEngineering.feature_extraction import apply_feature_extraction
from DataEngineering.preprocessing import appy_preprocess
import os

def apply_transformation(data):
    df = data.copy()
    numerical_cols = list(df.select_dtypes(exclude="object").columns)
    categorical_cols = list(df.select_dtypes(include="object").columns)

    # perform imputation
    if df.isnull().sum().sum() >= 1:
        try:
            print(f"{df.isnull().sum().sum()} null values exist in dataset. Performing imputation...")
            numerical_df = df[numerical_cols]
            categorical_df = df[categorical_cols]
            # for numerical cols
            num_imputer = SimpleImputer(strategy="median")
            # for categorical cols
            cat_imputer = SimpleImputer(strategy="most_frequent")
            # impute
            num_imputer = num_imputer.fit(numerical_df)
            cat_imputer = cat_imputer.fit(categorical_df)
            numerical_df = pd.DataFrame(num_imputer.transform(numerical_df), columns=numerical_cols)
            categorical_df = pd.DataFrame(cat_imputer.transform(categorical_df), columns=categorical_cols)
            # concat both dfs 
            df = pd.concat([numerical_df, categorical_df], axis=1)

        except Exception as e:
            print(f"Error while imputation: {e}")
    else:
        print("no null values exist. Ignoring Imputation")    
        
    # feature extraction
    print("Performing Feature Extraction...")
    df = apply_feature_extraction(data=df)
    print(f"columns after feature extraction: \n", df.info())

    numerical_cols = list(df.select_dtypes(exclude="object").columns)
    categorical_cols = list(df.select_dtypes(include="object").columns)

    # remove features having binary values from list
    if "placement_status" in numerical_cols:
        numerical_cols.remove("placement_status")
    if "academic_risk" in numerical_cols:
        numerical_cols.remove("academic_risk")
    if "placement_status" in categorical_cols:
        categorical_cols.remove("placement_status")
    
    # preprocessing 
    print("preprocessing dataset...")
    preprocessed_data = appy_preprocess(
        cat_cols=categorical_cols,
        num_cols=numerical_cols,
        data=df
    )

    return preprocessed_data


if __name__ == "__main__":

    SAVE_DIRECTORY = r"D:\projects\Student\dataset\processed"
    if not os.path.exists(SAVE_DIRECTORY):
        os.makedirs(SAVE_DIRECTORY)
    # 1. read the dataset
    try:
        df = pd.read_csv(r"D:\projects\Student\dataset\raw\data.csv")
        print("dataset load successful.")
    except FileNotFoundError:
        print(f"Error! File not Found")
    except Exception as e:
        print(f"Error: {e}")
    
    # 2. extract number from college_tier
    df["tier"] = df["college_tier"].str.split("-").str[1]
    # convert to integer
    df['tier'] = df['tier'].astype("int")
    # verify
    print(f"{df[['college_tier','tier']].head(5)}")
    print("data type: ", df['tier'].dtypes)

    # 3. remove "salary_package_lpa"
    df = df.drop(["salary_package_lpa","college_tier"], axis=1)
    # verify if removed
    print(f"columns: \n", df.columns)
    print("`salary_package_lpa`and `college_tier` dropped from data")

    # 4. preprocessing
    print("Applying preprocessing...")
    df = apply_transformation(data=df)

    # 5. save dataset into specific directory
    print(f"saving data to {SAVE_DIRECTORY}")
    df.to_csv(os.path.join(SAVE_DIRECTORY, "preprocessed_data.csv"), index=False)