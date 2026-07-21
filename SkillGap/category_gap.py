# calculates the gap for each category:
# 1. aptitude
# 2. projects
# 3. internships
# 4. soft skill

import pandas as pd
import numpy as np

def category_gap_calculation(domain, category_data):
    """
    *purpose*: to calculate the "category" gap from given input
    *input*: category_data (dataframe)
    *output*: 
    - total_technical_gap (float)
    - technical_gap_percent (float)
    - df (dataframe) : calculated gap for each category
    """
    df = category_data.copy()
    
    # calculation, avoid divide by zero
    df['category_gap'] = np.where(df['required'] == 0, 0, (df['required'] - df['student']) / df['required'])

    # clip negative gaps to 0
    df['category_gap'] = df['category_gap'].clip(lower=0)

    return df[['category', 'category_gap']]