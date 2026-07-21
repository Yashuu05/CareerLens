# calculates overall technical skill of a student
import pandas as pd
import numpy as np

def technical_skill_calculate(domain, skill_data):
    """
    *purpose*: to calculate the overall "technical" skill from given input
    *input*: skill_data (dataframe)
    *output*: 
    - total_technical_gap (float)
    - technical_gap_percent (float)
    - df (dataframe) : calculated gap for each skill
    """
    df = skill_data.copy()

    # calculation for each skill, handle division by zero if required is 0
    # Formula: weight * ((Required - Student) / Required)
    # If Student > Required, gap could be negative, meaning they over-index. We clip it at 0 to mean 0 gap, or keep negative. The pdf says 5-4/5 = 0.2. If 4-5/4 = -0.25 (meaning they exceed it). Usually gap is max(0, ...). 
    # Let's just follow the formula strictly as pdf doesn't mention max(0).
    df['gap'] = np.where(df['required'] == 0, 0, (df['required'] - df['student']) / df['required'])
    
    # clip negative gaps to 0 (if they have more skill than required, the gap is 0)
    df['gap'] = df['gap'].clip(lower=0)

    # multiply by weight
    df['gap'] = df['weight'] * df['gap']

    # final score
    total_technical_gap = float(df['gap'].sum())

    # percentage
    technical_gap_percent = float(total_technical_gap * 100)

    return total_technical_gap, technical_gap_percent, df[['skill', 'gap']]